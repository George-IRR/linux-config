# 17: PipeWire Audio Buffer Optimization

Documentation for applying a persistent, full-override configuration to PipeWire to resolve audio latency ("lag") issues. This method bypasses drop-in directory prioritization issues by directly establishing a primary user-level configuration file.

## Rationale
When PipeWire dynamically adjusts the buffer size (quantum) during operation, it can induce noticeable latency or audio dropouts. By forcing a standardized minimum and maximum quantum value, the hardware maintains a consistent processing state.

## Implementation: Full Configuration Override

To ensure persistence across system reboots, we construct a complete user-level duplicate of the master configuration.

1.  **Duplicate the Master Configuration:**
    Create a local override file by copying the system default into the user's configuration directory.
    ```bash
    cp /usr/share/pipewire/pipewire.conf ~/.config/pipewire/pipewire.conf
    ```

2.  **Edit the Configuration:**
    Open the newly created local file for modification.
    ```bash
    nano ~/.config/pipewire/pipewire.conf
    ```

3.  **Modify Quantum Parameters:**
    Locate the `context.properties` block within the file. Define the default clock quantum limits explicitly. Ensure these lines are uncommented (remove any leading `#`).

    Modify the block to reflect the following values:
    ```plaintext
    context.properties = {
        ## ... (other existing settings remain unchanged) ...

        default.clock.quantum       = 1024
        default.clock.min-quantum   = 1024
        default.clock.max-quantum   = 2048
    }
    ```
    *(Note: Equating `quantum` and `min-quantum` to 1024 prevents the daemon from dynamically downscaling the buffer, mitigating latency spikes).*

