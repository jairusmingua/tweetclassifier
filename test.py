from os import path

def main():
   print ("directory exists:" + str(path.exists('finetuned_model')))

if __name__== "__main__":
   main()