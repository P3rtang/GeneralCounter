from main import StartCounter
import os

main_path = os.path.abspath(__file__)
print(main_path)
os.chdir(main_path.replace('/main.pyw', ''))
StartCounter()
