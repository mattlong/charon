#!/bin/bash

./charon reset

./charon add-frontend app 0.0.0.0:80

./charon remove-frontend app

./charon add-frontend app 0.0.0.0:80

./charon add-backend app app1 1.1.1.1:80

./charon add-backend app app2 1.1.1.1:80

./charon remove-backend app app1

./charon disable app app2

./charon show
