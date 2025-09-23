from src.api import Yui
from src.backend import Cardinal

def main():
    Yui.app.run(debug=True)
    
    # Cardinal.requestsAllid()

if __name__ == "__main__":
    main()