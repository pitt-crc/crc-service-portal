"""Tests for the `DBHandler` class."""

import logging

from django.test import TestCase

from apps.logging.handlers import DBHandler
from apps.logging.models import AppLog


class EmitToDatabase(TestCase):
    """Test emitted log data is recorded into the application database."""

    def assert_db_record_matches_log_content(self, handler, log_record, db_record):
        """Assert the content of a database record matches the content of a log record

        Args:
            handler: The logging record used to format the log record
            log_record: The log record
            db_record: The database record
        """

        self.assertEqual(db_record.name, log_record.name)
        self.assertEqual(db_record.level, log_record.levelname)
        self.assertEqual(db_record.pathname, log_record.pathname)
        self.assertEqual(db_record.lineno, log_record.lineno)
        self.assertEqual(db_record.message, handler.format(log_record))
        self.assertEqual(db_record.func, log_record.funcName)
        self.assertEqual(db_record.sinfo, log_record.stack_info)

    def test_logs_to_database(self):
        """Test log data is recorded to the application database"""

        log_record = logging.LogRecord('test', logging.INFO, 'pathname', 1, 'message', (), None, 'func')
        handler = DBHandler()
        handler.emit(log_record)

        db_record = AppLog.objects.first()
        self.assert_db_record_matches_log_content(handler, log_record, db_record)

    def test_does_not_save_below_level(self):
        """Test log data is not saved when the log message level is below the logging threshold"""

        record = logging.LogRecord('test', logging.INFO, 'pathname', 1, 'message', (), None, 'func')
        handler = DBHandler(level=logging.ERROR)
        handler.emit(record)

        self.assertFalse(AppLog.objects.all())

    def test_saves_equal_to_level(self):
        """Test log data is saved when the log message level is equal to the logging threshold"""

        log_record = logging.LogRecord('test', logging.INFO, 'pathname', 1, 'message', (), None, 'func')
        handler = DBHandler(logging.INFO)
        handler.emit(log_record)

        db_record = AppLog.objects.first()
        self.assert_db_record_matches_log_content(handler, log_record, db_record)
