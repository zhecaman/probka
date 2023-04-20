import sqlite3



class BotDB:
    def __init__(self, db_file) -> None:
        """Initiate DB connection"""
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

    def user_exists_phone(self, phone_num : str)-> bool:
        '''Checking if user in DB'''
        with self.connection:
            result = self.cursor.execute('SELECT * FROM `users` WHERE `phone_num` = ?', (phone_num,))
            return bool(len(result.fetchall()))
    
    def user_exists_tg(self, tg_id):
        '''CHekking if user in DB by telegram userid'''
        with self.connection:
            result = self.cursor.execute('SELECT * FROM `users` WHERE `tg_id` = ?', (tg_id,))
            return bool(len(result.fetchall()))

    def get_id_code(self, phone_num : str)-> str:
        '''Getting a 6dig id code from DB'''
        with self.connection:
            result = self.cursor.execute('SELECT `user_id` FROM `users` WHERE `phone_num` = ?', (phone_num,))
            return result.fetchone()[0]
    
    def get_phone(self, user_id):
        with self.connection:
            result = self.cursor.execute('SELECT `phone_num` FROM `users` WHERE `user_id` = ?', (user_id,))
            return result.fetchone()[0]

    def add_nickname(self, nickname, phone_num):
        '''Adding user`s TG nickname to DB'''
        with self.connection:
            self.cursor.execute("UPDATE users SET 'nickname' = ? WHERE phone_num = ?", (nickname, phone_num))
            return self.connection.commit()
    

    def add_tg_id(self, tg_id, phone_num):
        """Adding users TG id to DB"""
        with self.connection:
            self.cursor.execute("UPDATE users SET 'tg_id' = ? WHERE phone_num = ?", (tg_id, phone_num))
            return self.connection.commit()
    



    def add_phone_and_code(self, phone_num, code):
        '''Adding into DB users phone and passcode'''
        with self.connection:
            self.cursor.execute('INSERT INTO `users` (`user_id`, `phone_num`) VALUES (?, ?)', (code, phone_num))
            return self.connection.commit()
        
    def all_users(self):
        with self.connection:
            result = self.cursor.execute('SELECT * FROM users `phone_num`')
            return result.fetchall()
     
    def close(self):
        self.connection.close()





                                 