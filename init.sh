
#!/bin/bash


update(){
	sudo apt-get update -y
	sudo apt-get upgrade -y
}


is_installed(){
        command -v $1 >/dev/null 2>&1
        echo $?
}

install_git(){
	if [ $(is_installed git) -eq 1 ] ; then
        	echo "sudo apt-get install git -y"
		# sudo apt-get install git -y
	else
		echo "git already installed";
		# :  # 'pass'
	fi
}


update
install_git








