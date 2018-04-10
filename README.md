# Repository for Python + Gurobi implementation of course scheduling problem for final project of DSO 570
Goal is to improve scheduling for USC.

- Current objective function is:
  - Maximize sum of x_ijk*(R_ik/C_jk)
    - Where x_ijk is our binary decision variable
    - R_ik is the required seating
    - C_jk is the room capacity

- Notes to include in final formulation:
  - Allow for flexibility in class time offering
  - Add relaxation of capacity for classroom (10% for most popular courses, 5% for more popular courses)
  - Account for professor preferences (separate optimization just used for professor to course time)
  - Course time to schedule for classrooms can then be ran
  - Department allocation addition
  - Additional classrooms not given in raw data can be scraped and used as subest
