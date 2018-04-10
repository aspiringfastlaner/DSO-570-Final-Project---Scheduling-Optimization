# Repository for Python + Gurobi implementation of course scheduling problem for final project of DSO 570
Goal is to improve scheduling for USC.
Within the current scheduling process, the most strenuous step is to properly allocate classrooms for the various courses. Not only is this a mentally taxing task, there is wastage in underutilized classrooms with the number of registered students below the classroom capacity. Additionally, classrooms are over capacity with populated waitlists. To take the fact that courses might be more popular than expected, and students might add the course later in the semester into consideration, we quantified the wastage of classrooms using the ratio of the number of seats offered to the classroom size, defined as our Utilization Ratio. Through the optimization of this Utilization Ratio, we hope to address this inefficiency while automating the process of classroom assignment.

- Notes to add:
Allow for flexibility in class time offering
Add relaxation of capacity for classroom (10% for most popular courses, 5% for more popular courses)
Account for professor preferences (separate optimization just used for professor to course time)
Course time to schedule for classrooms can then be ran
Department allocation addition
Additional classrooms not given in raw data can be scraped and used as subest
