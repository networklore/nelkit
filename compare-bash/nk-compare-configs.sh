#!/bin/bash
#==========================================================
# LANG : Bash
# NAME : nk-compare-configs.sh
# AUTHOR : Patrick Ogenstad
# VERSION : 1.0
# DATE : 2014-02-18
# Description : Parses network device configuration files
# and checks to see if your devices are configured in the
# same way.
#
# The Script is part of Nelkit (NetworkLore Toolkit)
# http://networklore.com/nelkit/
#
# Guidelines and updates:
# http://networklore.com/compare-router-configs/
#
# Feedback: Please send feedback:
# http://networklore.com/contact/
#
#==========================================================
#==========================================================

# Default settings 
RULESFILE="settings"
WORKDIR="work" 
BASELINE=""

SCRIPTVERSION="1.0"

bFINDWORKDIR="false"
bFINDBASELINE="false"
bFINDDEVICELIST="false"

#==========================================================
# Define functions 
#==========================================================

function check_distress {
  # Check to see if help has been requested
  if [ `echo "$1" | grep -E -c "^-h$|^help$|^--help$|^-help$"` -gt 0 ]; then
    display_help
  fi
}

function display_help {
  echo ""
  echo "nk-compare-configs.sh v.$SCRIPTVERSION"
  echo ""
  echo "Usage:"
  echo "./nk-compare-configs.sh"
  echo "./nk-compare-configs.sh rulesfile"
  echo "./nk-compare-configs.sh rulesfile configdir"
  echo "./nk-compare-configs.sh rulesfile configdir baselineconfig"
  echo "./nk-compare-configs.sh rulesfile configdir baselineconfig devlicelist"
  echo ""
  echo "Guidelines:"
  echo "You can run the script with 0-4 arguments. If you don't use any arguments"
  echo "the script will default to using a file called 'settings' in the current"
  echo "directory. The script will also default to looking in a directory called"
  echo "'work'. If you don't specify a baseline config file the script will choose"
  echo "the first file from the work directory. If you don't want the script to parse"
  echo "all of the files in the work directory you can point to a file containing"
  echo "a subset of your devices."
  echo ""
  echo "For more information and a howto guide which help you setup your settings"
  echo "file, visit:"
  echo ""
  echo "http://networklore.com/compare-router-configs/"
  echo ""
  exit
}
 
function match {
  MATCHSTRING="$1"
  RUN=1
  echo ""
  echo "--------------------------------------"
  echo "match"
  echo "string: $MATCHSTRING"
  echo "--------------------------------------"
  if [ "$bUSEBASELINE" = "true" ] ; then
   REFERENCE=`grep -E -- "$MATCHSTRING" $BASELINE`
  fi
  
  for DEVICE in $COLLECTION
  do
    if [ "$bUSEBASELINE" = "false" ] ; then
      if [ $RUN -eq 1 ]; then
        REFERENCE=`grep -E -- "$MATCHSTRING" $WORKDIR/$DEVICE`
      fi
    fi	
	
    CURRENT=`grep -E -- "$MATCHSTRING" $WORKDIR/$DEVICE`

    RUN=`expr $RUN + 1`
    DIFF=`diff  <(echo "$REFERENCE" ) <(echo "$CURRENT")`
	if [ `echo ${#DIFF}` -gt 0 ]; then
      echo "$DEVICE differs from baseline"
	fi
  done
}
 
function match_exclude {
  MATCHSTRING="$1"
  EXCLUDESTRING="$2"
  RUN=1

  echo ""
  echo "--------------------------------------"
  echo "match_exclude"
  echo "match: $MATCHSTRING"
  echo "exclude: $EXCLUDESTRING"
  echo "--------------------------------------"
  if [ "$bUSEBASELINE" = "true" ] ; then
    REFERENCE=`grep -E -- "$MATCHSTRING" $BASELINE | grep -E -v -- "$EXCLUDESTRING"` 
  fi
 
  for DEVICE in $COLLECTION
  do
    if [ "$bUSEBASELINE" = "false" ] ; then
      if [ $RUN -eq 1 ]; then
        REFERENCE=`grep -E -- "$MATCHSTRING" $WORKDIR/$DEVICE | grep -E -v -- "$EXCLUDESTRING"`
	  fi
    fi
    CURRENT=`grep -E -- "$MATCHSTRING" $WORKDIR/$DEVICE | grep -E -v -- "$EXCLUDESTRING"`
 
    RUN=`expr $RUN + 1`
    DIFF=`diff  <(echo "$REFERENCE" ) <(echo "$CURRENT")`
	if [ `echo ${#DIFF}` -gt 0 ]; then
      echo "$DEVICE differs from baseline"
	fi
  done
}

function match_sort {
  MATCHSTRING="$1"
  RUN=1
  echo ""
  echo "--------------------------------------"
  echo "match_sort"
  echo "string: $MATCHSTRING"
  echo "--------------------------------------"
  if [ "$bUSEBASELINE" = "true" ] ; then
   REFERENCE=`grep -E -- "$MATCHSTRING" $BASELINE | sort`
  fi
  
  for DEVICE in $COLLECTION
  do
    if [ "$bUSEBASELINE" = "false" ] ; then
      if [ $RUN -eq 1 ]; then
        REFERENCE=`grep -E -- "$MATCHSTRING" $WORKDIR/$DEVICE | sort`
      fi
    fi	
    CURRENT=`grep -E -- "$MATCHSTRING" $WORKDIR/$DEVICE | sort`

    RUN=`expr $RUN + 1`
    DIFF=`diff  <(echo "$REFERENCE" ) <(echo "$CURRENT")`
	if [ `echo ${#DIFF}` -gt 0 ]; then
      echo "$DEVICE differs from baseline"
	fi
  done
}

function match_exclude_sort {
  MATCHSTRING="$1"
  EXCLUDESTRING="$2"
  RUN=1

  echo ""
  echo "--------------------------------------"
  echo "match_exclude_sort"
  echo "match: $MATCHSTRING"
  echo "exclude: $EXCLUDESTRING"
  echo "--------------------------------------"
  if [ "$bUSEBASELINE" = "true" ] ; then
    REFERENCE=`grep -E -- "$MATCHSTRING" $BASELINE | grep -E -v -- "$EXCLUDESTRING" | sort` 
  fi
 
  for DEVICE in $COLLECTION
  do
    if [ "$bUSEBASELINE" = "false" ] ; then
      if [ $RUN -eq 1 ]; then
        REFERENCE=`grep -E -- "$MATCHSTRING" $WORKDIR/$DEVICE | grep -E -v -- "$EXCLUDESTRING" | sort`
	  fi
    fi
    CURRENT=`grep -E -- "$MATCHSTRING" $WORKDIR/$DEVICE | grep -E -v -- "$EXCLUDESTRING" | sort`
 
    RUN=`expr $RUN + 1`
    DIFF=`diff  <(echo "$REFERENCE" ) <(echo "$CURRENT")`
	if [ `echo ${#DIFF}` -gt 0 ]; then
      echo "$DEVICE differs from baseline"
	fi
  done
}
 
function start_end {
  BEGINSTRING="$1"
  ENDSTRING="$2"
  RUN=1

  echo ""
  echo "--------------------------------------"
  echo "start_end"
  echo "start: $BEGINSTRING"
  echo "end: $ENDSTRING"
  echo "--------------------------------------"
  if [ "$bUSEBASELINE" = "true" ] ; then
    REFERENCE=`sed -n "/$BEGINSTRING/,/$ENDSTRING/p" $BASELINE`
	if [ "${#REFERENCE}" = "0" ] ; then
		echo "No match found in reference"
	fi
  fi
 
  for DEVICE in $COLLECTION
  do
    if [ "$bUSEBASELINE" = "false" ] ; then
      if [ $RUN -eq 1 ]; then
        REFERENCE=`sed -n "/$BEGINSTRING/,/$ENDSTRING/p" $WORKDIR/$DEVICE`
  	    if [ "${#REFERENCE}" = "0" ] ; then
		  echo "No match found in reference"
	    fi
	  fi
    fi 

    CURRENT=`sed -n "/$BEGINSTRING/,/$ENDSTRING/p" $WORKDIR/$DEVICE`
    RUN=`expr $RUN + 1`
    DIFF=`diff  <(echo "$REFERENCE" ) <(echo "$CURRENT")`
	if [ `echo ${#DIFF}` -gt 0 ]; then
      echo "$DEVICE differs from baseline"
	fi
  done
}
 
function start_end_exclude {
  BEGINSTRING="$1"
  ENDSTRING="$2"
  EXCLUDESTRING="$3"
  RUN=1
 
  echo ""
  echo "--------------------------------------"
  echo "start_end_exclude"
  echo "start: $BEGINSTRING"
  echo "end: $ENDSTRING"
  echo "exclude: $EXCLUDESTRING"
  echo "--------------------------------------"
  if [ "$bUSEBASELINE" = "true" ] ; then
    REFERENCE=`sed -n "/$BEGINSTRING/,/$ENDSTRING/p" $BASELINE | grep -E -v -- "$EXCLUDESTRING"`
	if [ "${#REFERENCE}" = "0" ] ; then
		echo "No match found in reference"
	fi
  fi
 
  for DEVICE in $COLLECTION
  do
    if [ "$bUSEBASELINE" = "false" ] ; then
      if [ $RUN -eq 1 ]; then
        REFERENCE=`sed -n "/$BEGINSTRING/,/$ENDSTRING/p" $WORKDIR/$DEVICE  | grep -E -v -- "$EXCLUDESTRING"`
	    if [ "${#REFERENCE}" = "0" ] ; then
		  echo "No match found in reference"
	    fi
	  fi
    fi 

    CURRENT=`sed -n "/$BEGINSTRING/,/$ENDSTRING/p" $WORKDIR/$DEVICE  | grep -E -v -- "$EXCLUDESTRING"`
    RUN=`expr $RUN + 1`
    DIFF=`diff  <(echo "$REFERENCE" ) <(echo "$CURRENT")`
	if [ `echo ${#DIFF}` -gt 0 ]; then
      echo "$DEVICE differs from baseline"
	fi
  done
}

function verify_parameters {

  # Check to see if the rulesfile is readable
  if [ ! -r "$RULESFILE" ] ; then
    echo ""
	echo "## ERROR ########################################"
	echo "Unable to read settings from: $RULESFILE"
	echo "#################################################"
	display_help 
  fi

  # Check to see if the working directory should be read from the settings file
  if [ "$bFINDWORKDIR" = "true" ] ; then
    SETTINGSWORKDIR=`grep -- "^CONFIGDIR" "$RULESFILE" | cut -f 2 -d "=" | sed -r 's/"//g'`
    if [ `echo ${#SETTINGSWORKDIR}` -gt 0 ]; then
      WORKDIR="$SETTINGSWORKDIR"
    fi
  fi

  # Check to see if the working directory exists
  if [ ! -d "$WORKDIR" ]; then
    # Control will enter here if $DIRECTORY doesn't exist.
    echo ""
	echo "## ERROR ########################################"
	echo "Unable to read working directory: $WORKDIR"
	echo "#################################################"
	display_help 
  fi

  # Check to see if the baseline file should be read from the settings file
  if [ "$bFINDBASELINE" = "true" ] ; then
    SETTINGSBASELINE=`grep -- "^BASECONFIG" $RULESFILE | cut -f 2 -d "=" | sed -r 's/"//g'`
    if [ `echo ${#SETTINGSBASELINE}` -gt 0 ]; then
      BASELINE="$SETTINGSBASELINE"
    fi
  fi

  if [ `echo ${#BASELINE}` -gt 0 ]; then
    bUSEBASELINE="true"
	if [ `echo $BASELINE | grep -c "/"` -eq 0 ]; then
	  # A / is not included in the baseline setting, use baseline from workdir
	  BASELINE="$WORKDIR/$BASELINE"
	fi
      if [ ! -r "$BASELINE" ] ; then
        echo ""
        echo "## ERROR ########################################"
	    echo "Unable to read baseline file: $BASELINE"
	    echo "#################################################"
	    display_help 
    fi

  else
    bUSEBASELINE="false"
  fi
  
  # Check to see if a devicelist should be read from the settings file
  if [ "$bFINDDEVICELIST" = "true" ] ; then
    SETTINGSDEVICELIST=`grep -- "^DEVICEFILE" "$RULESFILE" | cut -f 2 -d "=" | sed -r 's/"//g'`
    if [ `echo ${#SETTINGSDEVICELIST}` -gt 0 ]; then
      DEVICELIST="$SETTINGSDEVICELIST"
    fi
  fi

  if [ `echo ${#DEVICELIST}` -gt 0 ]; then
    # Read from device list
    if [ ! -r "$DEVICELIST" ] ; then
      echo ""
	  echo "## ERROR ########################################"
      echo "Unable to read devicelist: $DEVICELIST"
      echo "#################################################"
      display_help 
    fi
    # Use a specific subset of working directory	
    COLLECTION=`cat $DEVICELIST`
  else
    # Use all of the devices in the workdir
    COLLECTION=`ls -1 $WORKDIR`	
  fi

  #Verify that we can read our collection
  for FILE in $COLLECTION
  do
  
    if [ ! -r "$WORKDIR/$FILE" ] ; then
      echo "## ERROR ########################################"
      echo "Unable to read the file: $WORKDIR/$FILE"
      echo "#################################################"
      display_help 	
    fi
  done

}

#==========================================================
# Main Script
#==========================================================

# Parse script arguments

if [ $# -gt 4 ] ; then
  echo "You have enterned too many arguments"
  display_help
elif [ $# -eq 4 ] ; then
  RULESFILE="$1"
  WORKDIR="$2"
  BASELINE="$3"
  DEVICELIST="$4"
elif [ $# -eq 3 ] ; then
  RULESFILE="$1"
  WORKDIR="$2"
  BASELINE="$3"
  bFINDDEVICELIST="true"
elif [ $# -eq 2 ] ; then
  RULESFILE="$1"
  WORKDIR="$2"
  bFINDBASELINE="true"
  bFINDDEVICELIST="true"
elif [ $# -eq 1 ] ; then
  RULESFILE="$1"
  bFINDWORKDIR="true"
  bFINDBASELINE="true"
  bFINDDEVICELIST="true"
elif [ $# -eq 0 ] ; then
  bFINDWORKDIR="true"
  bFINDBASELINE="true"
  bFINDDEVICELIST="true"
fi

check_distress $RULESFILE
check_distress $WORKDIR
check_distress $BASELINE
check_distress $DEVICELIST

verify_parameters

. $RULESFILE

