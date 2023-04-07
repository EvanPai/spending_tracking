import sys

class Record:
    """Represent a record."""
    #注意：category是一個string
    def __init__(self, category, item, amount):
        """Constructor of class Record"""
        self._category = category
        self._item = item
        self._amount = amount


    @property
    def category(self):
        """Return self._category"""
        return self._category
        
    #@category.setter
    #ef category(self, num):
    #    self._category = num    
    #r.category = 'food'

    @property
    def item(self):
        """Return self._item"""
        return self._item

    @property
    def amount(self):
        """Return self._amount"""
        return self._amount

class Records:
    """Maintain a list of all the 'Record's and the initial amount of money."""
    def __init__(self):
        """Constructor of Records"""
        balance = 0
        L = []
        try:
            with open('records.txt', 'r') as fh:
                #print('Open file records.txt')
                ib = fh.readline() # 讀取initial balance
                try: #exception 2
                    balance = int(ib)
                    
                except:
                    sys.stderr.write('Unable to read the initial balance. Set balance to 0 as default\n')
                    balance = 0 #初始化balance

                #開始讀入record
                for i in fh.readlines():
                    try:
                        i = i.strip() #strip()刪掉換行符號
                        note = i.split(':') #切掉:
                        cata = note[0] #前面是category
                        can = categories.is_category_valid(categories.get_categories(), cata)
                        if(can == False): 
                            sys.stderr.write('Invalid categories, unable to read an item \n')
                            continue

                        name = note[1] #中間是名字
                        money = int(note[2]) #後面是amount
                        r = Record(cata, name, money)
                        L.append(r)
                    except:
                        sys.stderr.write('Unable to read an item.\n')  
                
        except FileNotFoundError as err:
            sys.stderr.write(str(err) + '\n')
            sys.stderr.write('Initializing a new file...\n')
            #初始化一個檔案
            with open('records.txt', 'w') as fh:
                fh.write(str(balance) + '\n')

        try: #exception 3
            s1 = input('How much money do you have? ')
            balance = balance + int(s1)
        except (NameError, ValueError) as err:
            sys.stderr.write('Invalid value for money. append 0 by default\n')

        self._initial_money = balance
        self._records = L

    def add(self, s):
        """Add a record into self._records"""
        # 1. Define the formal parameter so that a string input by the user
    	#	representing a record can be passed in.
    	# 2. Convert the string into a Record instance.
    	# 3. Check if the category is valid. For this step, the predefined
    	#	categories have to be passed in through the parameter.
    	# 4. Add the Record into self._records if the category is valid.
        try: #exception 4
            Note = s.split(', ') #先切開', '
            #把資料轉存進L裡
            for i in Note:
                i2 = i.split(' ')
                

                cata = str(i2[0])
                #判斷category是否存在
                can = categories.is_category_valid(categories.get_categories(), cata)
                if(can == False): 
                    sys.stderr.write('Invalid categories, please try again: \n')
                    return


                item = str(i2[1])
                amount = int(i2[2])

                r = Record(cata, item, amount) #使用class Record
                
                self._records.append(r) #丟進records裡
                self._initial_money += amount #增加money值

        except:
            sys.stderr.write('The format of a record should be like this: meal breakfast -50. Fail to add a record.\n')

    def view(self):
        """Print out all the records and current balance"""
        # 1. Print all the records and report the balance.
        print("Here's your expense and income records:")
        print('category          Description          Amount')
        print('================= ==================== ======')
        for i in self._records:
            print( '%-18s'%i.category + '%-21s'%i.item + str(i.amount))
        print('=============================================')
        print(f'Balance : {self._initial_money}')

    def delete(self, s):
        """delete a record"""
        # 1. Define the formal parameter.
    	# 2. Delete the specified record from self._records.
        #target = int(s)
        try: #exception 5
            #輸入要刪掉第幾個
            if int(s) > 0:
                self._initial_money -= int(self._records[int(s)-1].amount)
                self._records.pop(int(s)-1)
            else: #exception 6
                sys.stderr.write('Invalid number. Should be > 0.\n')
        except ValueError as err: #exception 7
            sys.stderr.write('Invalid format. Fail to delete a record.\n')
        except IndexError as err: #exception 8
            sys.stderr.write('There are only %d elements in list. Please try again.\n'%len(self._records))

    def find(self, target):
        """Print out the specific category records"""
        # 1. Define the formal parameter to accept a non-nested list
    	#	(returned from find_subcategories)
    	# 2. Print the records whose category is in the list passed in
    	#	and report the total amount of money of the listed records.
        #todo
        #sub = categories.find_subcategories(target, categories.get_categories())
        if(target == []):
            print("Invalid category, please try again: ")
            return
        #sub回傳一個flat List
        print(f"Here's your expense and income records under category \"{target[0]}\":")
        print('category          Description          Amount')
        print('================= ==================== ======')
        balance = 0
        i2 = filter(lambda x : x.category in target, self._records)
        for i in i2:
        #for i in self._records:
            #if(i.category in target):
            print( '%-18s'%i.category + '%-21s'%i.item + str(i.amount))
            balance += int(i.amount)
        print('=============================================')
        print(f'Balance : {balance}')

    def save(self):
        """Save all the records into records.txt"""
    	# 1. Write the initial money and all the records to 'records.txt'.
        #存檔
        try: #exception 10
            with open('records.txt', 'w') as fh:
                #print('Open file records')
                #先寫入balance
                fh.write(str(self._initial_money)+'\n')

                #再寫入其他項目
                for i in self._records:
                    #分別寫入category:item:amount
                    s = str(i.category) + ':' + str(i.item) + ':' + str(i.amount) + '\n'
                    fh.write(s)
            
        except FileNotFoundError as err:
            sys.stderr.write(str(err) + '\n')


class Categories:
    """Maintain the category list and provide some methods."""
    def __init__(self):
         # 1. Initialize self._categories as a nested list.
        self._categories = ['expense', ['food', ['meal', 'snack', 'drink'], 'transportation', ['bus', 'railway']], 'income', ['salary', 'bonus']]
        
    def get_categories(self):
        """Return self._categories"""
        return self._categories

    def view(self, C, level=0):
        """Print out the categories hierarchy"""
        # 1. Define the formal parameters so that this method
    	#	can be called recursively.
    	# 2. Recursively print the categories with indentation.
    	# 3. Alternatively, define an inner function to do the recursion.
        if C == None:
            return
        if(type(C) in {list, tuple}):
            for i in C:
                self.view(i, level+1)
        else:
            print(f'{" "*2*level + "- "}{C}')


    def is_category_valid(self, C, target):
        """Check whether a category is valid"""
    	# 1. Define the formal parameters so that a category name can be
    	#	passed in and the method can be called recursively.
    	# 2. Recursively check if the category name is in self._categories.
    	# 3. Alternatively, define an inner function to do the recursion.
        

        def valid(C, target):
            if(type(C) != list):
                if(target == C): return 1
                else: return 0

            count = 0 
            for i in C:
                count += valid(i, target)

            return count
        
        ans = valid(C, target)
        if(ans >= 1): return True
        else: return False

        #if(type(C) in {list, tuple}):
        #    for i in C:
        #         self.is_category_valid(i)
        #else:#來判斷target是否在self._categories中
        #    if(target == C): return True


    def find_subcategories(self, category, categories):
        """Find the subcategories under a category"""
        # 1. Define the formal parameters so that a category name can be
    	#	passed in and the method can be called recursively.
    	# 2. Recursively find the target category and call the
    	#	self._flatten method to get the subcategories into a flat list.
    	# 3. Alternatively, define an inner function to do the recursion.
        def find_subcategories_gen(category, categories, found=False):
            """Use generator to find subcategories"""
            if type(categories) == list: # recursive case
                for index, child in enumerate(categories):
                    yield from find_subcategories_gen(category, child, found)
                    if child == category and index + 1 < len(categories) and type(categories[index + 1]) == list:
                        # When the target category is found,
                        # recursively call this generator on the subcategories
                        # with the flag set as True.
                        yield from find_subcategories_gen(category, categories[index+1], True)
            else: # base cases
                if categories == category or (found == True):
                    yield categories

        return list(find_subcategories_gen(category, categories, False))

        
categories = Categories()
records = Records()

while True:

    command = input('\nWhat do you want to do (add / view / delete / view categories / find / exit)? ')
    if command == 'add':
        record = input('Add an expense or income record with (category item amount): ')
        records.add(record)
    elif command == 'view':
        records.view()
    elif command == 'delete':
        delete_record = input("Which record do you want to delete? ")
        records.delete(delete_record)
    elif command == 'view categories':
        categories.view(categories.get_categories())
    elif command == 'find':
        category = input('Which category do you want to find? ')
        #print(categories.get_categories())
        target_categories = categories.find_subcategories(category, categories.get_categories())
        #print(target_categories)
        records.find(target_categories)
    elif command == 'exit':
        records.save()
        break
    else:
        sys.stderr.write('Invalid command. Try again.\n')