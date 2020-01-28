Exercise-1
==========

Write an Ansible print_name module to print full name as task output.
1) The module should have first, middle (optional), last as arguments
2) Should return complete name in module result.
3) If first or last arguments is not received as input from user module should throw an error.

Exercise-2
==========

Extend Ansible print_name module to print full name with title as task output.
1) Add a new argument title
2) The accepted values of title are Mr, Mrs, Ms.
3) The title argument and middle argument should be mutually exculsive, that is if
   user inputs both title and middle argument module should throw an error.
