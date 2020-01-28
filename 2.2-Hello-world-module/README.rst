Exercise-1
==========

Write an Ansible print_name module to print full name as task output.
* The module should have first, middle (optional), last as arguments
* Should return complete name in module result.
* If first or last arguments is not received as input from user module should throw an error.

Exercise-2
==========

Extend Ansible print_name module to print full name with title as task output.
* Add a new argument title
* The accepted values of title are Mr, Mrs, Ms.
* The title argument and middle argument should be mutually exculsive, that is if
   user inputs both title and middle argument module should throw an error.
