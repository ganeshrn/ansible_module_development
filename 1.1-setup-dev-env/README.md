## Access the Environment

Login to your control host via SSH:

> **Warning**
>
> Replace **11.22.33.44** by your **IP** provided to you, and the **X** in student**X** by the student number provided to you.

    ssh studentX@11.22.33.44


Then become root:

    [student<X>@ansible ~]$ sudo -i

Most prerequisite tasks have already been done for you:

  - Ansible software is installed

  - SSH connection and keys are configured

  - `sudo` has been configured on the managed hosts to run commands that require root privileges.

Check Ansible has been installed correctly

    [root@ansible ~]# ansible --version
    ansible 2.7.0


## Edit ~/.vimrc before starting

* Append contents of VIMRC from current directory to your ~/.vimrc

