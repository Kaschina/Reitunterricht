#!/usr/bin/python

'''
# kurzes skript, das die tagebucheingabe vereinfachen soll(te)
# automatische Commits
'''
import csv
import argparse
import shutil
from fabric.api import run, env, local


def add_new_event(kalender, date, was, positiv, negativ):
    with open(kalender, 'ra') as csvfile, open("tmp.csv", "a") as outputfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        writer = csv.writer(outputfile, delimiter=',')
        for row in spamreader:
            if row[1] == date:
                row[2] = was
                row[3] = positiv
                row[4] = negativ

            writer.writerow(row)
    shutil.move("tmp.csv", kalender)
    make_commit(date)

def make_commit(datum):
    env.host = ['localhost']
    local('cd /home/melanie/Repositories/Reitunterricht/')
    local('git commit -am "' + datum + '"')
    local('git push origin master')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-k", "--kal", help="Kalender-Datei", required=True)
    parser.add_argument("-d", "--date", help="welcher Tag", required=True)
    parser.add_argument("-w", "--was", help="was hast du gemacht")
    parser.add_argument("-p", "--positiv", help="was war positiv")
    parser.add_argument("-n", "--negativ", help="was war negativ")

    args = parser.parse_args()

    kalender = args.kal
    date     = args.date
    was      = args.was
    positiv  = args.positiv
    negativ  = args.negativ

    #print kalender + " " + date + "" + was + "" +positiv + " " + negativ
    add_new_event(kalender, date, was, positiv, negativ)

if __name__ == "__main__":
    main()
