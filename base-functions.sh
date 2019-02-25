#!/bin/bash -x
function cook_package {
action=$1
name=$2

installed=$(aptitude -q=10 search -F %p "~i ?name(^$name$)")

if [[ "$action" == "install" &&  -z "$installed" ]]; then
    echo "installing $name"
    apt-get -y install "$name"
fi

if [[ "$action" == "remove" && -n "$installed" ]]; then
    echo "removing $name"
    apt-get -y autoremove "$name"
fi

}

function cook_file {
action=$1
path=$2
temppath=$3

if [[ $action == "create" ]]; then
    echo "creating $path"
    mv $temppath $path
fi

if [[ -e $path && $action == "remove" ]]; then
    echo "removing $path"
    rm -f $path
fi
}

