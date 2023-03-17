## How to execute the project and the tests?

The only dependency of the project is `pytest`. Therefore the project can run as long as you have python on the machine.

The project has a **Makefile** with which you can run all the implemented functionalities.

### Run Command

To execute the main functionality of the project, the **Makefile** has a `run` command that expects a **file** variable as input. This variable must be the address of the file to be read.

```bash
$> make run file=example.txt
```

If this parameter is not assigned, the program will launch a **FormatError**. On the other hand the assigned value is not the address of a file that can be opened, the sys library will launch the appropriate error.

### Run_test Command

The project was implemented following some of the **TDD** philosophy guidelines. Therefore a collection of tests were implemented to guarantee the integrity of the system. To execute these tests the **Makefile** has the command `run_test`.

In this case, before executing this command you must install the above mentioned dependency. This project was developed in a **pipenv** environment with python 3.10. But so that the user is not tied to the use of these technologies also offers a **requirements.txt** file with all the necessary dependencies.

Therefore, the user can either integrate all the dependencies or with the following command:

```bash
$> pipenv install
```

Or with this one:

```bash
$> pip install -r requirements.txt
```

After all the dependencies are installed just run the following command to run all the tests

```bash
$> make run_test
```

## Project structure

The project is separated by layers. Each layer is responsible for a single responsibility and defines a series of communication protocols with the layers on which it may depend. Basic idea of **Clean Architecture**

- **Interpretation Layer**: This layer is in charge of parsing and checking the syntax and semantics of each of the commands that are read in the program input. This layer communicates with the persistence layer. After analyzing all the information provided by the input, this layer creates instances of the different models of the system and passes them to the persistence layer so that it stores this information.

- **Persistence Layer**: This layer is in charge of storing all the information provided by the input and maintaining the state of the program according to the different operations requested. In this implementation this layer presents an implementation in memory. But the decoupling of the solution must be such that it is very simple to change to another more durable in the time.

- **Application Layer**: This layer is functionally oriented, composed of a list of use cases. For the given problem only one is needed, but with this functional approach adding functionalities is equivalent to implementing a new function. This layer consumes system information by querying the persistence layer.

## Visitor Pattern

The Interpretation and Persistence Layers were both implemented through a hierarchy of classes, one class per command, and an extra class that implements the visitor pattern supported by the Python `functools` library.

The problem posed can be interpreted as a sequence of commands given to a state machine. The commands are executed one after the other and each one has its own rules depending on the state of the system.

Under such a description the visitor pattern is a great tool to present a highly maintainable and extensible solution. The visitor pattern proposes the definition of a function for each entity of the domain, defining a single point of entry to each layer which must be in charge of selecting which is the function that must be executed according to the type of the entry.

In this way, not only the procedures of each command can be decoupled among them, but also a change of technology, such as the selection of a new tool for persistence, implies only the definition of a new class with a function for each type of the domain.

## Notes

During the implementation some doubts sometimes arise about the problem domain. Doubts on which some assumptions were made:

- The format of the commands will be as defined. Only being flexible with the number of spaces between the command components. So the implementation will be case-sensitive.
- It was considered that some information in the commands could be altered or erroneous. In that sense it was controlled that:
  - the input time is less than the output time of all **Presence** commands. In this case, an `InformationError` will be triggered
  - the occurrence of **Presence** commands describing overlapping time frames. In this case the information will be marked as a **Warning** but the analysis of each case will be performed to calculate the time of the student in the school considering the overlapping valid.
