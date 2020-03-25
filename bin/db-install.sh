#!/usr/local/bin/bash
brew install postgres
brew services start postgresql
psql postgres
