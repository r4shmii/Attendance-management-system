# Problem Statement

Manually taking and tracking attendance on paper registers is time consuming
and error prone. Teachers often struggle to quickly calculate attendance
percentages or find out which students are falling below the required
attendance limit. This project aims to solve that with a simple, easy to use
command-line application.

## Scope of the Project

This project covers basic attendance tracking for a single class/section.
It does not connect to any external database or web service, and it does not
have a graphical interface — everything is done through the terminal using
simple menu options. Data is stored locally using CSV files.

## Target Users

- Teachers or class coordinators who want a quick way to record daily
  attendance without maintaining paper registers.
- Students/small institutes that don't have access to a full attendance
  management software.

## High-Level Features

- Student registration (add and view students)
- Daily attendance marking (present/absent)
- Date-wise attendance lookup
- Attendance percentage report for every student
- Automatic detection of students below the minimum attendance requirement (75%)
