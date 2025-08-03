Startup time in Python
$ time python3 main.py
real    0m0.463s
user    0m0.015s
sys     0m0.045s
(.venv) 

Startup time in Go
2025/07/30 21:20:56 ✅ Connected to PostgreSQL
2025/07/30 21:20:56 📦 inventory-service ready in 2.6305ms

#Go (powershell)
tasklist | findstr inventory
inventory-service             5992 Console                    1      8,692 K

#python (powershell)
tasklist | findstr python
python.exe                   13764 Console                    1     25,404 K
python.exe                   14100 Console                    1     48,024 K

#Go (powershell)
Get-Item .\inventory-service | Select-Object Name, Length

Name                Length
----                ------
inventory-service 10421760

#python (powershell)
(.venv) PS G:\compare-go-with-python> du -sh .venv
40M     .venv
(.venv) PS G:\compare-go-with-python> (Get-ChildItem .venv -Recurse | Measure-Object -Property Length -Sum).Sum / 1MB
34.5643110275269