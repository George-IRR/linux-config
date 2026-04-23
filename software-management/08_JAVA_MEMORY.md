# 08: Java Memory Allocation

Heap size limit control for `.jar` executables. Prevents sudden process termination (crashes) caused by RAM exhaustion (Out of Memory).

## Execution Parameters

* `-Xms`: Defines the initial memory allocated at application startup.
* `-Xmx`: Defines the maximum RAM limit the application can request.

## Application

Execute the application by explicitly defining parameters before specifying the file.

Example allocation (512 MB initial, 2048 MB maximum limit):
```bash
java -Xms512M -Xmx2048M -jar application.jar
```