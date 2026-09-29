# Building Characteristics Input Form — Spec

## Overview

This feature is a data entry form. It's the first point that we get data from the user.

It gets data from the user and makes sure that they are valid data. For example, postal code is
in Germany, building age is less than 300 years old. This feature does not involve other
components like user id and other stuff.

## Interface

Several entry boxes dedicated to each one of:

- Location (zip code)
- Area (m²)
- Building's age
- Heating type
- Windows type (1/2/3 layer)

## Validation rules

- Zip code must be within Germany and an integer.
- Area must be an integer and less than 500.
- Building age must be an integer and less than 300.
- Heating type and windows type must be chosen from drop-down lists.

## Prerequisites

As this is the first step, no prerequisites needed.

## After this step

The data for these entries will get their new value.

## Error / confirmation behavior

- If the inputs are wrong and don't match the specification, the user should see an error to
  correct their input.
- If the inputs are right, show a confirmation message to the user.
