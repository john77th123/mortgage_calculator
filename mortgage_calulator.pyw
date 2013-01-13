from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys, os, sip, math
    
class paymentCalculator(QMainWindow):
    def __init__(self, parent=None):
        super(paymentCalculator, self).__init__(parent)
        self.mainWidget = QWidget()
        self.setCentralWidget(self.mainWidget)
        self.mainLayout = QVBoxLayout()
        self.mainWidget.setLayout(self.mainLayout)
        
        self.setObjectName("jlMortgageCalculator")
        
        #Mortgage item part
        self.mortgageLayout = QVBoxLayout()
        self.mortgageItems = [
                         "LoanAmount",
                         "InterestRate",
                         "Term",
                         "HOA",
                         "Tax",
                         "Insurance"
                         ]
        
        #Add items to mortgage layout
        for cur in self.mortgageItems:
            self.addItem(cur, self.mortgageLayout)
        
        self.mainLayout.addLayout(self.mortgageLayout)
        #separator
        line = QFrame()
        line.setFrameStyle(QFrame.HLine | QFrame.Sunken )
        self.mainLayout.addWidget(line)
        
        #Monthly item part
        self.itemLayout = QVBoxLayout()
        self.items = [
                "Food",
                "Allowances",
                "Verizon",
                "Utility",
                "AutoInsurace",
                "Cable",
                "Gas"
                 ]
        #Add items to monthly item layout
        for cur in self.items:
            self.addItem(cur, self.itemLayout)
        
        self.mainLayout.addLayout(self.itemLayout)
        
        #Add item button
        self.addItemLayout  = QHBoxLayout()
        self.addItemButton = QPushButton(text = "+")
        self.addItemButton.setFixedWidth(25)
        self.addItemLayout.addWidget(self.addItemButton)

        self.addItemLabel = QLabel(text="Add Item")
        self.addItemLabel.setFixedWidth(80)
        
        self.addItemValue = QLineEdit()
        self.addItemValue.setPlaceholderText("Item Name")
        self.addItemValue.setMinimumWidth(100)
        
        self.addItemButton.clicked.connect(self.addNewItem)

        self.addItemLayout.addWidget(self.addItemLabel)
        self.addItemLayout.addWidget(self.addItemValue)
        
        self.mainLayout.addLayout(self.addItemLayout)
 
        line = QFrame()
        line.setFrameStyle(QFrame.HLine | QFrame.Sunken )
        self.mainLayout.addWidget(line)

        self.houseExpenseLayout = QVBoxLayout()
        self.houseExpenseLabel = QLabel("Total House Payment")
        self.houseExpenseValue = QLineEdit()
        
        self.houseExpenseLayout.addWidget(self.houseExpenseLabel)
        self.houseExpenseLayout.addWidget(self.houseExpenseValue)
        
        self.mainLayout.addLayout(self.houseExpenseLayout)

        self.monthlyExpenseLayout = QVBoxLayout()
        self.monthlyExpenseLabel = QLabel("Monthly Expenses")
        self.monthlyExpenseValue = QLineEdit()
        
        self.monthlyExpenseLayout.addWidget(self.monthlyExpenseLabel)
        self.monthlyExpenseLayout.addWidget(self.monthlyExpenseValue)
        
        self.mainLayout.addLayout(self.monthlyExpenseLayout)
        
        self.monthlyTotalExpenseLayout = QVBoxLayout()
        self.monthlyTotalExpenseLabel = QLabel("Total Monthly Expenses")
        self.monthlyTotalExpenseValue = QLineEdit()
        
        self.monthlyTotalExpenseLayout.addWidget(self.monthlyTotalExpenseLabel)
        self.monthlyTotalExpenseLayout.addWidget(self.monthlyTotalExpenseValue)
        
        self.mainLayout.addLayout(self.monthlyTotalExpenseLayout)
        
        calculateButton = QPushButton(text="Calculate")
        self.mainLayout.addWidget(calculateButton)
        calculateButton.clicked.connect(self.calculate)
        
        setDefaultButton = QPushButton(text="Set Default")
        self.mainLayout.addWidget(setDefaultButton)
        setDefaultButton.clicked.connect(self.setDefault)
        self.setDefault()
    
    def addNewItem(self):
        item = self.addItemValue.text()
        if item:
            item = str(item)
            if item not in self.items:
                self.addItem(item, self.itemLayout)
                self.items.append(item)
                
            
    def addItem(self, item, layoutToAdd):        
        layout  = QHBoxLayout()
        setattr(self, item + "Layout", layout)
        layout = getattr(self, item + "Layout")
        
        if item not in self.mortgageItems:
            button = QPushButton(text = "-")
            setattr(self, item + "Button", button)
            button = getattr(self, item + "Button")
            button.setFixedWidth(25)
            button.setObjectName(item + "Button")
            button.clicked.connect(self.removeItem)
            layout.addWidget(button)
            
        label = QLabel(text=item)
        setattr(self, item + "Label", label)
        label = getattr(self, item + "Label")
        label = QLabel(text=item)
        label.setFixedWidth(80)
        
        edit = QLineEdit()
        setattr(self, item + "Value", edit)
        value = getattr(self, item + "Value")
        value.setMinimumWidth(100)

        layout.addWidget(label)
        layout.addWidget(value)
        
        layoutToAdd.addLayout(layout)
              
    def removeItem(self):
        #layoutName = str(self.sender().objectName().replace("Button", "Layout"))
        itemName = str(self.sender().objectName().replace("Button", ""))
        layoutName = str(self.sender().objectName().replace("Button", "Layout"))
        layout = getattr(self, layoutName)
        
        for i in reversed(range(layout.count())):
            item = layout.itemAt(i)
    
            if isinstance(item, QWidgetItem):
                item.widget().close()
                # or
                # item.widget().setParent(None)
            elif isinstance(item, QSpacerItem):
                pass
                # no need to do extra stuff
            else:
                self.clearLayout(item.layout())
                
            layout.removeItem(item)       
        
        self.items.remove(itemName)
        self.calculate()
        
    def setDefault(self):
        self.LoanAmountValue.setText("320000")
        self.InterestRateValue.setText("3.7")
        self.TermValue.setText("360")
        self.HOAValue.setText("250")
        self.TaxValue.setText("300")
        self.InsuranceValue.setText("60")
        
        self.FoodValue.setText("500")
        self.AllowancesValue.setText("200")
        self.VerizonValue.setText("120")
        self.UtilityValue.setText("100")
        self.AutoInsuraceValue.setText("100")
        self.CableValue.setText("60")
        self.GasValue.setText("300")
        self.calculate()
        
    def calculate(self):
        returnResults = []
        for cur in self.mortgageItems:
            value = getattr(self, cur + "Value").text()
            if value:
                returnResults.append(float(value))
            else:
                returnRestults.append(0)
        result = self.printPayment(returnResults[0], returnResults[1]/1200, returnResults[2], returnResults[3], returnResults[4], returnResults[5])
        self.houseExpenseValue.setText(str(result[0]))
        self.monthlyExpenseValue.setText(str(result[1]))
        self.monthlyTotalExpenseValue.setText(str(result[2]))
        
    
    def printPayment(self, loanAmount, interestRate, term, tax=0, hoa=0, insurance=0, income=0):
        houseExpense = (loanAmount* (interestRate*math.pow((1+interestRate),term))) / (math.pow((1+interestRate),term) -1) + tax + hoa + insurance

        expenseTotal = 0
        for cur in self.items:
            value = getattr(self, cur + "Value").text()
            if value:
                expenseTotal += float(value)
 
        totalMonthlyExpense = houseExpense + expenseTotal
        print "House expense total is %f"%houseExpense
        print "Monthly expense total is %f"%expenseTotal
        print "Total monthly expense total is %f"%totalMonthlyExpense
        print "Your monthly income is %f. Gee... make some more money dude."%income
        
        if totalMonthlyExpense > income:
            difference = totalMonthlyExpense - income
            print "Don't even think about it. You are %f short. "%difference
            
        else:
            difference = income - totalMonthlyExpense
            print "Yeah, you can afford this house and have plenty money left over like %f"%difference
        
        return houseExpense, expenseTotal, totalMonthlyExpense
    
    
if __name__ == "__main__":
    app = QApplication([])   
    window = paymentCalculator()
    window.show()
    sys.exit(app.exec_())
