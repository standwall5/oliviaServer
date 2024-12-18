from flask import Flask, request, jsonify
import psycopg2

conn = psycopg2.connect(host="dpg-ctgh6ergbbvc738q4gh0-a.singapore-postgres.render.com", dbname="oliviadb_3q1f", user="olivia", password="UQOeX7M9u6BNtKWbfhQ4kUl5txdCQ1gt", port=5432)

cur = conn.cursor()