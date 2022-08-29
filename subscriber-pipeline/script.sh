#!/bin/bash


# prompts the user to confirm before cleansing the data
echo "Ready to clean the data? [1/0]"
read cleancontinue

# if the user selects 1 then run the cleanse_data script
if [ $cleancontinue -eq 1 ]
then
    echo "Cleaning Data"
    python dev/cleanse_data.py
    echo "Done Cleaning Data"

    # grab the first line of dev and prod changelogs
    dev_version=$(head -n 1 dev/changelog.md)
    prod_version=$(head -n 1 prod/changelog.md)

    # delimit the 1st line of the changelog by space
    read -a splitversion_dev <<< $dev_version
    read -a splitversion_prod <<< $prod_version

    # delimiting will result in a list of two elements
    # the second (index 1) will contain the version numbers
    dev_version=${splitversion_dev[1]}
    prod_version=${splitversion_prod[1]}

    if [ $prod_version != $dev_version ]
    then
        # Tells the user that the dev and prod changes are different
        # ask before proceeding to move dev files to prod
        echo "New changes detected. Move dev files to prod? [1/0]"
        read scriptcontinue
    else
        scriptcontinue=0
    fi
# otherwise, don't run anything
else
    echo "Please come back when you are ready"
fi

# if user selects 1 then copy or move certain files from dev to prod
if [ $scriptcontinue -eq 1 ]
then
    for filename in dev/*
    do
        if [ $filename == "dev/cademycode_cleansed.db" ] || [ $filename == "dev/cademycode_cleansed.csv" ] || [ $filename == "dev/changelog.md" ]
        then
            cp $filename prod
            echo "Copying " $filename
        else
            echo "Not Copying " $filename
        fi
    done
# otherwise, don't run anything
else
    echo "Please come back when you are ready"
fi
