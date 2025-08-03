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
"{0:N2} MB" -f ((Get-Item .\inventory-service).Length / 1MB)
9.94 MB


#python (powershell)
"{0:N2} MB" -f ((Get-ChildItem -Recurse .\.venv | Measure-Object -Property Length -Sum).Sum / 1MB)
34.56 MB