#!/bin/bash

DB_FILE="users.db"
BACKUP_DIR="/tmp/backups"
LOG_FILE="backup.log"

function log_message() {
    echo "$(date) - $1" >> $LOG_FILE   # ❌ No quoting
}

function init() {
    if [ ! -d $BACKUP_DIR ]; then
        mkdir $BACKUP_DIR   # ❌ No error handling / no -p
    fi

    if [ ! -f $DB_FILE ]; then
        touch $DB_FILE
    fi
}

function add_user() {
    username=$1
    password=$2

    echo "$username:$password" >> $DB_FILE   # ❌ Plaintext password storage
    log_message "User $username added"
}

function delete_user() {
    username=$1
    grep -v "^$username:" $DB_FILE > temp.db && mv temp.db $DB_FILE  # ❌ Unsafe temp file
    log_message "User $username deleted"
}

function list_users() {
    cat $DB_FILE
}

function backup_db() {
    timestamp=$(date +%s)
    backup_file="$BACKUP_DIR/backup_$timestamp.db"

    cp $DB_FILE $backup_file   # ❌ No validation
    log_message "Backup created at $backup_file"
}

function restore_db() {
    file=$1

    cp $file $DB_FILE   # ❌ No validation / path traversal risk
    log_message "Database restored from $file"
}

function find_user() {
    username=$1
    grep "$username" $DB_FILE   # ❌ Regex injection risk
}

function login() {
    username=$1
    password=$2

    stored=$(grep "^$username:" $DB_FILE | cut -d':' -f2)

    if [ "$stored" == "$password" ]; then
        echo "Login successful"
    else
        echo "Invalid credentials"
    fi
}

function cleanup_old_backups() {
    days=$1
    find $BACKUP_DIR -type f -mtime +$days -exec rm {} \;   # ❌ Dangerous rm usage
    log_message "Old backups cleaned"
}

function export_users() {
    file=$1
    cp $DB_FILE $file   # ❌ No validation
    log_message "Users exported to $file"
}

function import_users() {
    file=$1
    cat $file >> $DB_FILE   # ❌ No validation / duplicates
    log_message "Users imported from $file"
}

function menu() {
    while true; do
        echo "1. Add User"
        echo "2. Delete User"
        echo "3. List Users"
        echo "4. Backup DB"
        echo "5. Restore DB"
        echo "6. Find User"
        echo "7. Login"
        echo "8. Cleanup Backups"
        echo "9. Export Users"
        echo "10. Import Users"
        echo "11. Exit"

        read -p "Enter choice: " choice

        case $choice in
            1)
                read -p "Username: " u
                read -p "Password: " p
                add_user $u $p   # ❌ Unquoted variables
                ;;
            2)
                read -p "Username: " u
                delete_user $u
                ;;
            3)
                list_users
                ;;
            4)
                backup_db
                ;;
            5)
                read -p "Backup file path: " f
                restore_db $f
                ;;
            6)
                read -p "Username: " u
                find_user $u
                ;;
            7)
                read -p "Username: " u
                read -p "Password: " p
                login $u $p
                ;;
            8)
                read -p "Days: " d
                cleanup_old_backups $d
                ;;
            9)
                read -p "Export file: " f
                export_users $f
                ;;
            10)
                read -p "Import file: " f
                import_users $f
                ;;
            11)
                break
                ;;
            *)
                echo "Invalid choice"
                ;;
        esac
    done
}

# Main Execution
init
menu
