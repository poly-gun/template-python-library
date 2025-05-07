# ====================================================================================
# Example Makefile Template
# ------------------------------------------------------------------------------------

SHELL := /usr/bin/env bash

# ====================================================================================
# Colors
# ------------------------------------------------------------------------------------

black        := $(shell printf "\033[30m")
black-bold   := $(shell printf "\033[30;1m")
red          := $(shell printf "\033[31m")
red-bold     := $(shell printf "\033[31;1m")
green        := $(shell printf "\033[32m")
green-bold   := $(shell printf "\033[32;1m")
yellow       := $(shell printf "\033[33m")
yellow-bold  := $(shell printf "\033[33;1m")
blue         := $(shell printf "\033[34m")
blue-bold    := $(shell printf "\033[34;1m")
magenta      := $(shell printf "\033[35m")
magenta-bold := $(shell printf "\033[35;1m")
cyan         := $(shell printf "\033[36m")
cyan-bold    := $(shell printf "\033[36;1m")
white        := $(shell printf "\033[37m")
white-bold   := $(shell printf "\033[37;1m")
reset        := $(shell printf "\033[0m")

# ====================================================================================
# Logger
# ------------------------------------------------------------------------------------

time-long	= $(date +%Y-%m-%d' '%H:%M:%S)
time-short	= $(date +%H:%M:%S)
time		= $(time-short)

information	= echo $(time) $(blue)[ DEBUG ]$(reset)
warning	= echo $(time) $(yellow)[ WARNING ]$(reset)
exception		= echo $(time) $(red)[ ERROR ]$(reset)
complete		= echo $(time) $(green)[ COMPLETE ]$(reset)
fail	= (echo $(time) $(red)[ FAILURE ]$(reset) && false)

# ====================================================================================
# Utility Command(s)
# ------------------------------------------------------------------------------------

url = $(shell git config --get remote.origin.url | sed -r 's/.*(\@|\/\/)(.*)(\:|\/)([^:\/]*)\/([^\/\.]*)\.git/https:\/\/\2\/\4\/\5/')

repository = $(shell basename -s .git $(shell git config --get remote.origin.url))
organization = $(shell git remote -v | grep "(fetch)" | sed 's/.*\/\([^ ]*\)\/.*/\1/')
package = $(shell printf "github.com/%s/%s" "$(organization)" "$(repository)")

version = $(shell [ -f VERSION ] && head VERSION || echo "0.0.0")

major      		= $(shell echo $(version) | sed "s/^\([0-9]*\).*/\1/")
minor      		= $(shell echo $(version) | sed "s/[0-9]*\.\([0-9]*\).*/\1/")
patch      		= $(shell echo $(version) | sed "s/[0-9]*\.[0-9]*\.\([0-9]*\).*/\1/")

zero = $(shell printf "%s" "0")

major-upgrade 	= $(shell expr $(major) + 1).$(zero).$(zero)
minor-upgrade 	= $(major).$(shell expr $(minor) + 1).$(zero)
patch-upgrade 	= $(major).$(minor).$(shell expr $(patch) + 1)

dirty = $(shell git diff --quiet)
dirty-contents 			= $(shell git diff --shortstat 2>/dev/null 2>/dev/null | tail -n1)

# ====================================================================================
# Package-Specific Target(s)
# ------------------------------------------------------------------------------------

all :: no-op

no-op:
	@echo $(red)No-Operation$(reset)
