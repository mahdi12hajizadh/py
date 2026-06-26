"""
سیستم مدیریت بانک - Bank Management System
نسخه کامل با امکانات پیشرفته
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Optional


class Bank:
    """کلاس اصلی بانک برای مدیریت حساب‌ها"""
    
    id_carts = 1000
    transactions_history = []  # تاریخچه تمام تراکنش‌ها
    
    def __init__(self, name: str, balance: float = 0, password: str = "1234"):
        """
        ایجاد حساب جدید بانکی
        
        Args:
            name (str): نام صاحب حساب
            balance (float): موجودی اولیه (پیش‌فرض 0)
            password (str): رمز عبور (پیش‌فرض 1234)
        """
        self.__name = name
        self.__balance = balance
        self.__id_cart = Bank.id_carts
        self.__password = password
        self.__is_active = True
        self.__created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.__transactions = []  # تاریخچه تراکنش‌های این حساب
        
        # ثبت تراکنش اولیه
        if balance > 0:
            self._add_transaction("افتتاح حساب", balance, balance)
        
        Bank.id_carts += 1
        print(f"✅ حساب با موفقیت ایجاد شد! شماره کارت: {self.__id_cart}")

    # ============ Property ها ============
    
    @property
    def balance(self) -> float:
        """دریافت موجودی حساب (فقط خواندنی)"""
        return self.__balance
    
    @property
    def id_cart(self) -> int:
        """دریافت شماره کارت (فقط خواندنی)"""
        return self.__id_cart
    
    @property
    def name(self) -> str:
        """دریافت نام صاحب حساب (فقط خواندنی)"""
        return self.__name
    
    @property
    def is_active(self) -> bool:
        """وضعیت فعال بودن حساب"""
        return self.__is_active
    
    @property
    def transactions(self) -> List[Dict]:
        """دریافت تاریخچه تراکنش‌ها (فقط خواندنی)"""
        return self.__transactions.copy()
    
    @property
    def created_at(self) -> str:
        """تاریخ ایجاد حساب"""
        return self.__created_at

    # ============ متدهای داخلی ============
    
    def _add_transaction(self, type: str, amount: float, new_balance: float):
        """ثبت تراکنش جدید در تاریخچه"""
        transaction = {
            "type": type,
            "amount": amount,
            "balance": new_balance,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "account": self.__id_cart
        }
        self.__transactions.append(transaction)
        Bank.transactions_history.append(transaction)
    
    def _verify_password(self, password: str) -> bool:
        """تأیید رمز عبور"""
        return self.__password == password

    # ============ متدهای اصلی ============
    
    def deposit(self, amount: float, password: str = None) -> str:
        """
        واریز وجه به حساب
        
        Args:
            amount (float): مبلغ واریز
            password (str): رمز عبور (اختیاری)
        
        Returns:
            str: پیام نتیجه
        """
        # اگر رمز عبور داده نشده، نیازی به تأیید نیست (برای امنیت بیشتر)
        if password and not self._verify_password(password):
            return "❌ رمز عبور اشتباه است!"
        
        if amount <= 0:
            return "❌ مبلغ واریز باید بزرگتر از صفر باشد!"
        
        if not self.__is_active:
            return "❌ حساب شما غیرفعال است!"
        
        self.__balance += amount
        self._add_transaction("واریز", amount, self.__balance)
        return f"✅ مبلغ {amount:,.0f} تومان با موفقیت واریز شد!\n   موجودی جدید: {self.__balance:,.0f} تومان"
    
    def withdraw(self, amount: float, password: str) -> str:
        """
        برداشت وجه از حساب
        
        Args:
            amount (float): مبلغ برداشت
            password (str): رمز عبور (الزامی)
        
        Returns:
            str: پیام نتیجه
        """
        if not self._verify_password(password):
            return "❌ رمز عبور اشتباه است!"
        
        if amount <= 0:
            return "❌ مبلغ برداشت باید بزرگتر از صفر باشد!"
        
        if not self.__is_active:
            return "❌ حساب شما غیرفعال است!"
        
        if amount > self.__balance:
            return f"❌ موجودی ناکافی! موجودی شما: {self.__balance:,.0f} تومان"
        
        self.__balance -= amount
        self._add_transaction("برداشت", -amount, self.__balance)
        return f"✅ مبلغ {amount:,.0f} تومان با موفقیت برداشت شد!\n   موجودی جدید: {self.__balance:,.0f} تومان"
    
    def transfer(self, target_bank: 'Bank', amount: float, password: str) -> str:
        """
        انتقال وجه به حساب دیگر
        
        Args:
            target_bank (Bank): شیء بانک مقصد
            amount (float): مبلغ انتقال
            password (str): رمز عبور (الزامی)
        
        Returns:
            str: پیام نتیجه
        """
        # اعتبارسنجی‌ها
        if not self._verify_password(password):
            return "❌ رمز عبور اشتباه است!"
        
        if amount <= 0:
            return "❌ مبلغ انتقال باید بزرگتر از صفر باشد!"
        
        if not self.__is_active:
            return "❌ حساب شما غیرفعال است!"
        
        if not target_bank.is_active:
            return "❌ حساب مقصد غیرفعال است!"
        
        if amount > self.__balance:
            return f"❌ موجودی ناکافی! موجودی شما: {self.__balance:,.0f} تومان"
        
        if self.__id_cart == target_bank.id_cart:
            return "❌ نمی‌توانید به خودتان انتقال دهید!"
        
        # انجام انتقال
        self.__balance -= amount
        target_bank._Bank__balance += amount  # دسترسی به متغیر خصوصی
        
        # ثبت تراکنش‌ها
        self._add_transaction(f"انتقال به {target_bank.name} ({target_bank.id_cart})", -amount, self.__balance)
        target_bank._add_transaction(f"دریافت از {self.__name} ({self.__id_cart})", amount, target_bank.balance)
        
        return f"""✅ انتقال با موفقیت انجام شد!
   مبلغ: {amount:,.0f} تومان
   از: {self.__name} ({self.__id_cart})
   به: {target_bank.name} ({target_bank.id_cart})
   موجودی جدید شما: {self.__balance:,.0f} تومان"""
    
    def get_transactions(self, limit: int = 10) -> str:
        """
        دریافت تاریخچه تراکنش‌ها
        
        Args:
            limit (int): تعداد آخرین تراکنش‌ها
        
        Returns:
            str: تاریخچه تراکنش‌ها
        """
        if not self.__transactions:
            return "📭 هیچ تراکنشی ثبت نشده است!"
        
        last_transactions = self.__transactions[-limit:]
        
        result = f"📊 تاریخچه تراکنش‌های حساب {self.__id_cart} (آخرین {len(last_transactions)} تراکنش):\n"
        result += "=" * 60 + "\n"
        
        for t in reversed(last_transactions):
            icon = "➕" if t["amount"] > 0 else "➖" if t["amount"] < 0 else "📌"
            result += f"{icon} {t['type']:20} | {t['amount']:>12,} تومان | {t['date']}\n"
        
        result += "=" * 60
        return result
    
    def change_password(self, old_password: str, new_password: str) -> str:
        """
        تغییر رمز عبور
        
        Args:
            old_password (str): رمز فعلی
            new_password (str): رمز جدید
        
        Returns:
            str: پیام نتیجه
        """
        if not self._verify_password(old_password):
            return "❌ رمز عبور فعلی اشتباه است!"
        
        if len(new_password) < 4:
            return "❌ رمز جدید باید حداقل 4 کاراکتر باشد!"
        
        self.__password = new_password
        return "✅ رمز عبور با موفقیت تغییر کرد!"
    
    def deactivate_account(self, password: str) -> str:
        """
        غیرفعال کردن حساب
        
        Args:
            password (str): رمز عبور
        
        Returns:
            str: پیام نتیجه
        """
        if not self._verify_password(password):
            return "❌ رمز عبور اشتباه است!"
        
        if not self.__is_active:
            return "⚠️ حساب شما قبلاً غیرفعال شده است!"
        
        self.__is_active = False
        return f"⚠️ حساب {self.__id_cart} با موفقیت غیرفعال شد!"
    
    def activate_account(self, password: str) -> str:
        """
        فعال کردن مجدد حساب
        
        Args:
            password (str): رمز عبور
        
        Returns:
            str: پیام نتیجه
        """
        if not self._verify_password(password):
            return "❌ رمز عبور اشتباه است!"
        
        if self.__is_active:
            return "ℹ️ حساب شما قبلاً فعال است!"
        
        self.__is_active = True
        return f"✅ حساب {self.__id_cart} با موفقیت فعال شد!"

    # ============ متدهای جادویی ============
    
    def __str__(self) -> str:
        """نمایش اطلاعات حساب به صورت رشته"""
        status = "فعال ✅" if self.__is_active else "غیرفعال ❌"
        return f"""
📋 مشخصات حساب بانکی:
═══════════════════════════════════
   👤 نام: {self.__name}
   🆔 شماره کارت: {self.__id_cart}
   💰 موجودی: {self.__balance:,.0f} تومان
   📅 تاریخ ایجاد: {self.__created_at}
   📊 وضعیت: {status}
═══════════════════════════════════
"""
    
    def __repr__(self) -> str:
        """نمایش خلاصه اطلاعات"""
        return f"Bank(name='{self.__name}', id={self.__id_cart}, balance={self.__balance})"

    # ============ متدهای کلاس ============
    
    @classmethod
    def get_all_transactions(cls) -> str:
        """دریافت تاریخچه تمام تراکنش‌های همه حساب‌ها"""
        if not cls.transactions_history:
            return "📭 هیچ تراکنشی ثبت نشده است!"
        
        result = f"📊 تاریخچه کل تراکنش‌های سیستم ({len(cls.transactions_history)} تراکنش):\n"
        result += "=" * 70 + "\n"
        
        for t in cls.transactions_history:
            icon = "➕" if t["amount"] > 0 else "➖" if t["amount"] < 0 else "📌"
            result += f"{icon} حساب {t['account']:4} | {t['type']:25} | {t['amount']:>12,} تومان | {t['date']}\n"
        
        result += "=" * 70
        return result
    
    @classmethod
    def save_to_file(cls, accounts: List['Bank'], filename: str = "bank_data.json"):
        """
        ذخیره اطلاعات در فایل JSON
        
        Args:
            accounts (List[Bank]): لیست حساب‌ها
            filename (str): نام فایل
        """
        data = {
            "accounts": [],
            "total_carts": cls.id_carts
        }
        
        for acc in accounts:
            data["accounts"].append({
                "name": acc.__name,
                "balance": acc.__balance,
                "id_cart": acc.__id_cart,
                "password": acc.__password,
                "is_active": acc.__is_active,
                "created_at": acc.__created_at,
                "transactions": acc.__transactions
            })
        
        try:
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"✅ اطلاعات با موفقیت در {filename} ذخیره شد!")
        except Exception as e:
            print(f"❌ خطا در ذخیره‌سازی: {e}")
    
    @classmethod
    def load_from_file(cls, filename: str = "bank_data.json") -> List['Bank']:
        """
        بارگذاری اطلاعات از فایل JSON
        
        Args:
            filename (str): نام فایل
        
        Returns:
            List[Bank]: لیست حساب‌ها
        """
        accounts = []
        
        if not os.path.exists(filename):
            print(f"⚠️ فایل {filename} یافت نشد!")
            return accounts
        
        try:
            with open(filename, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            cls.id_carts = data.get("total_carts", 1000)
            
            for acc_data in data["accounts"]:
                # ایجاد حساب جدید
                acc = cls(acc_data["name"], acc_data["balance"], acc_data["password"])
                acc._Bank__id_cart = acc_data["id_cart"]  # تنظیم شماره کارت
                acc._Bank__is_active = acc_data["is_active"]
                acc._Bank__created_at = acc_data["created_at"]
                acc._Bank__transactions = acc_data["transactions"]
                accounts.append(acc)
            
            print(f"✅ {len(accounts)} حساب از {filename} بارگذاری شد!")
            
        except Exception as e:
            print(f"❌ خطا در بارگذاری: {e}")
        
        return accounts


# ============================================================
# بخش مدیریت بانک (سیستم مدیریت کامل)
# ============================================================

class BankManager:
    """سیستم مدیریت کامل بانک"""
    
    def __init__(self):
        self.accounts: List[Bank] = []
        self.current_account: Optional[Bank] = None
        self.logged_in = False
    
    def create_account(self, name: str, initial_balance: float = 0, password: str = "1234") -> Bank:
        """
        ایجاد حساب جدید
        
        Args:
            name (str): نام
            initial_balance (float): موجودی اولیه
            password (str): رمز عبور
        
        Returns:
            Bank: حساب ایجاد شده
        """
        account = Bank(name, initial_balance, password)
        self.accounts.append(account)
        return account
    
    def login(self, id_cart: int, password: str) -> str:
        """
        ورود به حساب
        
        Args:
            id_cart (int): شماره کارت
            password (str): رمز عبور
        
        Returns:
            str: پیام نتیجه
        """
        for acc in self.accounts:
            if acc.id_cart == id_cart:
                if acc._verify_password(password):
                    self.current_account = acc
                    self.logged_in = True
                    return f"✅ به حساب {acc.name} خوش آمدید!"
                else:
                    return "❌ رمز عبور اشتباه است!"
        
        return "❌ شماره کارت یافت نشد!"
    
    def logout(self) -> str:
        """خروج از حساب"""
        if self.logged_in:
            name = self.current_account.name
            self.current_account = None
            self.logged_in = False
            return f"✅ از حساب {name} خارج شدید!"
        return "ℹ️ شما وارد سیستمی نشده‌اید!"
    
    def get_all_accounts(self) -> str:
        """نمایش تمام حساب‌ها"""
        if not self.accounts:
            return "📭 هیچ حسابی ثبت نشده است!"
        
        result = "📋 لیست تمام حساب‌های بانکی:\n"
        result += "=" * 60 + "\n"
        
        for acc in self.accounts:
            status = "✅" if acc.is_active else "❌"
            result += f"{status} {acc.id_cart:5} | {acc.name:15} | {acc.balance:>12,} تومان\n"
        
        result += "=" * 60
        return result
    
    def search_account(self, keyword: str) -> List[Bank]:
        """
        جستجوی حساب بر اساس نام یا شماره کارت
        
        Args:
            keyword (str): عبارت جستجو
        
        Returns:
            List[Bank]: لیست حساب‌های پیدا شده
        """
        result = []
        keyword = keyword.lower()
        
        for acc in self.accounts:
            if keyword in str(acc.id_cart) or keyword in acc.name.lower():
                result.append(acc)
        
        return result


# ============================================================
# منوی کاربری (برای اجرای مستقیم)
# ============================================================

def main():
    """منوی اصلی برنامه"""
    manager = BankManager()
    
    # ایجاد چند حساب نمونه
    print("🏦 در حال ایجاد حساب‌های نمونه...")
    manager.create_account("علی رضایی", 1000000, "1234")
    manager.create_account("مریم حسینی", 500000, "5678")
    manager.create_account("رضا کریمی", 2000000, "9012")
    print("✅ ۳ حساب نمونه ایجاد شد!\n")
    
    while True:
        print("\n" + "=" * 50)
        print("🏦 سیستم مدیریت بانک - PythonSchool")
        print("=" * 50)
        print("1. ایجاد حساب جدید")
        print("2. ورود به حساب")
        print("3. خروج از حساب")
        print("4. مشاهده همه حساب‌ها")
        print("5. جستجوی حساب")
        print("6. مشاهده تاریخچه کل تراکنش‌ها")
        print("7. ذخیره اطلاعات")
        print("8. بارگذاری اطلاعات")
        print("0. خروج")
        print("=" * 50)
        
        choice = input("🔹 انتخاب کنید: ").strip()
        
        if choice == "0":
            print("👋 خداحافظ!")
            break
        
        elif choice == "1":
            name = input("👤 نام و نام خانوادگی: ").strip()
            try:
                balance = float(input("💰 موجودی اولیه (تومان): ").strip())
            except ValueError:
                balance = 0
            password = input("🔑 رمز عبور (حداقل 4 کاراکتر): ").strip()
            if len(password) < 4:
                print("❌ رمز عبور باید حداقل 4 کاراکتر باشد!")
                continue
            account = manager.create_account(name, balance, password)
        
        elif choice == "2":
            try:
                id_cart = int(input("🆔 شماره کارت: ").strip())
            except ValueError:
                print("❌ شماره کارت نامعتبر!")
                continue
            password = input("🔑 رمز عبور: ").strip()
            result = manager.login(id_cart, password)
            print(result)
            
            if manager.logged_in:
                # منوی داخلی حساب
                while True:
                    print("\n" + "-" * 40)
                    print(f"👤 خوش آمدید {manager.current_account.name}")
                    print("-" * 40)
                    print("1. نمایش اطلاعات حساب")
                    print("2. واریز وجه")
                    print("3. برداشت وجه")
                    print("4. انتقال وجه")
                    print("5. تاریخچه تراکنش‌ها")
                    print("6. تغییر رمز عبور")
                    print("7. غیرفعال کردن حساب")
                    print("8. فعال کردن حساب")
                    print("9. بازگشت به منوی اصلی")
                    print("-" * 40)
                    
                    sub_choice = input("🔹 انتخاب کنید: ").strip()
                    
                    if sub_choice == "9":
                        manager.logout()
                        break
                    
                    elif sub_choice == "1":
                        print(manager.current_account)
                    
                    elif sub_choice == "2":
                        try:
                            amount = float(input("💰 مبلغ واریز (تومان): ").strip())
                        except ValueError:
                            print("❌ مبلغ نامعتبر!")
                            continue
                        result = manager.current_account.deposit(amount)
                        print(result)
                    
                    elif sub_choice == "3":
                        try:
                            amount = float(input("💰 مبلغ برداشت (تومان): ").strip())
                        except ValueError:
                            print("❌ مبلغ نامعتبر!")
                            continue
                        password = input("🔑 رمز عبور: ").strip()
                        result = manager.current_account.withdraw(amount, password)
                        print(result)
                    
                    elif sub_choice == "4":
                        try:
                            target_id = int(input("🆔 شماره کارت مقصد: ").strip())
                        except ValueError:
                            print("❌ شماره کارت نامعتبر!")
                            continue
                        
                        # پیدا کردن حساب مقصد
                        target = None
                        for acc in manager.accounts:
                            if acc.id_cart == target_id:
                                target = acc
                                break
                        
                        if not target:
                            print("❌ حساب مقصد یافت نشد!")
                            continue
                        
                        try:
                            amount = float(input("💰 مبلغ انتقال (تومان): ").strip())
                        except ValueError:
                            print("❌ مبلغ نامعتبر!")
                            continue
                        
                        password = input("🔑 رمز عبور: ").strip()
                        result = manager.current_account.transfer(target, amount, password)
                        print(result)
                    
                    elif sub_choice == "5":
                        try:
                            limit = int(input("🔢 تعداد تراکنش‌های اخیر (پیش‌فرض 10): ").strip() or 10)
                        except ValueError:
                            limit = 10
                        print(manager.current_account.get_transactions(limit))
                    
                    elif sub_choice == "6":
                        old = input("🔑 رمز فعلی: ").strip()
                        new = input("🔑 رمز جدید (حداقل 4 کاراکتر): ").strip()
                        result = manager.current_account.change_password(old, new)
                        print(result)
                    
                    elif sub_choice == "7":
                        password = input("🔑 رمز عبور برای تأیید: ").strip()
                        result = manager.current_account.deactivate_account(password)
                        print(result)
                    
                    elif sub_choice == "8":
                        password = input("🔑 رمز عبور برای تأیید: ").strip()
                        result = manager.current_account.activate_account(password)
                        print(result)
                    
                    else:
                        print("❌ گزینه نامعتبر!")
        
        elif choice == "3":
            if manager.logged_in:
                result = manager.logout()
                print(result)
            else:
                print("ℹ️ شما وارد سیستمی نشده‌اید!")
        
        elif choice == "4":
            print(manager.get_all_accounts())
        
        elif choice == "5":
            keyword = input("🔍 عبارت جستجو (نام یا شماره کارت): ").strip()
            results = manager.search_account(keyword)
            if results:
                print(f"✅ {len(results)} حساب پیدا شد:")
                for acc in results:
                    print(f"   🆔 {acc.id_cart} | {acc.name} | {acc.balance:,.0f} تومان")
            else:
                print("❌ حسابی یافت نشد!")
        
        elif choice == "6":
            print(Bank.get_all_transactions())
        
        elif choice == "7":
            if manager.accounts:
                Bank.save_to_file(manager.accounts)
            else:
                print("⚠️ هیچ حسابی برای ذخیره وجود ندارد!")
        
        elif choice == "8":
            loaded = Bank.load_from_file()
            if loaded:
                manager.accounts = loaded
                print("✅ اطلاعات با موفقیت بارگذاری شد!")
        
        else:
            print("❌ گزینه نامعتبر!")


# ============================================================
# اجرای برنامه
# ============================================================

if __name__ == "__main__":
    main()