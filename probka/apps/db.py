import sqlite3



class BotDB:
    def __init__(self, db_file) -> None:
        """Initiate DB connection"""
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

    def user_exists(self, phone_num):
        '''Checking if user in DB'''
        result = self.cursor.execute('SELECT `id` FROM `users` WHERE `phone_num` = ?', (phone_num,))
        return bool(len(result.fetchall()))
    
    
    def get_id_code(self, phone_num):
        '''Getting a 6dig id code from DB'''
        result = self.cursor.execute('SELECT `user_id` FROM `users` WHERE `phone_num` = ?', (phone_num,))
        return result.fetchone()[0]
    
    def get_phone(self, user_id):
        result = self.cursor.execute('SELECT `phone_num` FROM `users` WHERE `user_id` = ?', (user_id,))
        return result.fetchone()

    def add_nickname(self, nickname, phone_num):
        '''Adding user`s TG nickname to DB'''
        self.cursor.execute('UPDATE `users` SET (`nickname`) = ? WHERE `phone_num` = ?', (nickname, phone_num))
        return self.connection.commit()
    
    def add_phone_and_code(self, phone_num, code):
        '''Adding into DB users phone and passcode'''
        self.cursor.execute('INSERT INTO `users` (`user_id`, `phone_num`) VALUES (?, ?)', (code, phone_num))
        return self.connection.commit()

    def get_phones_list(self):
        '''Get full list of users phone numbers'''
        result = self.cursor.execute('SELECT `phone_num` FROM `users`')
        return result.fetchall()
    
    def get_nicknames(self):
        result = self.cursor.execute('SELECT `nickname` FROM `users`')
        return result.fetchall()
    
    def close(self):
        self.connection.close()





                                 