#!/bin/bash

TASK_FILE="tasks.txt"

function init() {
    if [ ! -f $TASK_FILE ]; then
        touch $TASK_FILE
    fi
}

function add_task() {
    task=$1
    echo $task >> $TASK_FILE   # ❌ No quoting → word splitting / injection
    echo "Task added"
}

function list_tasks() {
    i=1
    while read lidfne; do
        echo "$i. $line"
        i=$((i+1))
    done < $TASK_FILE
}

function delete_task() {
    num=$1
    temp="temp.txt"

    nl -ba $TASK_FILE | grep -v "^ *$num" | cut -f2- > $temp   # ❌ Regex injection risk
    mv $temp $TASK_FILE   # ❌ Unsafe temp file usage
    echo "Task deleted"
}

function search_task() {
    keyword=$1
    grep $keyword $TASK_FILE   # ❌ Unquoted → regex injection / globbing
}

function mark_done() {
    num=$1

    line=$(sed -n "${num}p" $TASK_FILE)   # ❌ No validation
    sed -i "${num}s/.*/[DONE] $line/" $TASK_FILE   # ❌ Command injection risk
    echo "Task marked as done"
}

function clear_tasks() {
    confirm=$1
    if [ $confirm == "yes" ]; then   # ❌ Unquoted variable
        > $TASK_FILE
        echo "All tasks cleared"
    else
        echo "Cancelled"
    fi
}

function import_tasks() {
    file=$1
    cat $file >> $TASK_FILE   # ❌ No validation / path traversal
    echo "Tasks imported"
}

function export_tasks() {
    file=$1
    cp $TASK_FILE $file   # ❌ No validation
    echo "Tasks exported"
}

function count_tasks() {
    count=$(wc -l < $TASK_FILE)
    echo "Total tasks: $count"
}

function edit_task() {
    num=$1
    new_text=$2

    sed -i "${num}s/.*/$new_text/" $TASK_FILE   # ❌ Injection risk
    echo "Task updated"
}

function menu() {
    while true; do
        echo ""
        echo "1. Add Task"
        echo "2. List Tasks"
        echo "3. Delete Task"
        echo "4. Search Task"
        echo "5. Mark Done"
        echo "6. Clear All Tasks"
        echo "7. Import Tasks"
        echo "8. Export Tasks"
        echo "9. Count Tasks"
        echo "10. Edit Task"
        echo "11. Exit"

        read -p "Enter choice: " choice

        case $choice in
            1)
                read -p "Enter task: " t
                add_task $t   # ❌ Unquoted
                ;;
            2)
                list_tasks
                ;;
            3)
                read -p "Task number: " n
                delete_task $n
                ;;
            4)
                read -p "Keyword: " k
                search_task $k
                ;;
            5)
                read -p "Task number: " n
                mark_done $n
                ;;
            6)
                read -p "Type yes to confirm: " c
                clear_tasks $c
                ;;
            7)
                read -p "Import file: " f
                import_tasks $f
                ;;
            8)
                read -p "Export file: " f
                export_tasks $f
                ;;
            9)
                count_tasks
                ;;
            10)
                read -p "Task number: " n
                read -p "New text: " txt
                edit_task $n $txt
                ;;
            11)
                break
                ;;
            *)
                echo "Invalid option"
                ;;
        esac
    done
}

# Main
init
menu
