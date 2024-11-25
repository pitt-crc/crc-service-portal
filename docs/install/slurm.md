# Configuring Slurm

Slurm categorizes system usage in terms of trackable resources (TRES).
Keystone uses these TRES values to enforces allocation limits in the Slurm scheduler.
The total billable TRES for a given Slurm job is determined as a sum over the TRES usage $\left ( U \right )$ scaled by an administrator defined billing weight $\left ( W \right )$ :

$$ 
\text{Billable Usage} = \sum_\text{TRES} \,\, \left ( W_\text{TRES} * U_\text{TRES} \right )
$$

Keystone interfaces with Slurm to automatically enforce per-cluster limits on a group's total allowed *Billable Usage*.
When a group reaches their allocation limit, their Slurm jobs will no longer get scheduled on the target cluster.

Keystone is agnostic to most Slurm settings, and requires minimal modification to a running Slurm cluster.
However, certain fairshare features are incompatible with the Keystone accounting system and must be disabled.
The steps below walk through the necessary setup and configuration for a successful integration.

## Enable Resource Tracking

For Keystone to impose a usage limit on a computational resource, that resource must be represented in Slurm as a TRES.
Resource tracking for common TRES' like CPU, memory, and energy usage is enabled by default.
However, administrators may wish to extend the default list to enable limits on additional resource types (e.g., for GPU usage).

The `AccountingStorageTRES` setting is used to extend the default list of TRES values stored in the Slurm database.
See the official [Surm documentation](https://slurm.schedmd.com/tres.html#conf) on `slurm.conf` settings for details.

??? Example "Example: Tracking GPU usage"

    The following example enables tracking for GPU resources in addition to the default TRES tracked by slurm.

    ```
    AccountingStorageTRES=gres/gpu
    ```

??? Example "Example: Tracking GPU and IOP"

    The following example extends the default TRES list with resources called GPU and iop1.

    ```
    AccountingStorageTRES=gres/gpu,license/iop1
    ```

## Disable Usage Decay

Slurm defaults to using the [multifactor priority plugin](https://slurm.schedmd.com/priority_multifactor.html) to schedule jobs.
This can be confirmed by checking the Slurm `PriorityType` setting.

```bash
scontrol show config | grep PriorityType
```

When using the multifactor plugin, the `PriorityDecayHalfLife` and `PriorityUsageResetPeriod` settings need to be disabled.
Leaving either of these features enabled will cause Slurm to periodically reduce an account's recorded resource usage, causing inaccuracies in resource allocation limits. 

```
PriorityDecayHalfLife=00:00:00
PriorityUsageResetPeriod=NONE
```

!!! Important

    Disabling the `PriorityDecayHalfLife` and `PriorityUsageResetPeriod` values may affect your Slurm fairshare policy.
    Administrators should adjust the rest of their fairshair policy settings as they see appropriate. 

## Configure Charging Rates

TRES billing weights default to zero and are set on a per-partition basis using the `TRESBillingWeights` setting.
Billing weights are definable in variety of units. 
See the [Slurm documentation](https://slurm.schedmd.com/tres.html) for more details.

??? Example "Example: Billing for CPU"

    The following example only charges users for CPU resources.

    ```
    PartitionName=partition_name TRESBillingWeights="CPU=1.0"
    ```

??? Example "Example: Billing for CPU and GPU"

    The following example charges users for GPU resources at twice the rate of CPU resources.

    ```
    PartitionName=partition_name TRESBillingWeights="CPU=1.0,GRES/gpu=2.0"
    ```

To ensure the total allocated resources are calculated correctly, the `MAX_TRES` flag must be enabled. 
Doing so ensures the billable TRES include individual TRES on a node (e.g. cpus, mem, gres) plus the sum of all global TRES (e.g. licenses).

```
PriorityFlags=MAX_TRES
```
