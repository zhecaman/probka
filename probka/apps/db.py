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
    
    def get_user_id(self, user_id):
        '''Gettig user id from DB based on his telegram id'''
        result = self.cursor.execute('SELECT `id` FROM `users` WHERE `user_id` = ?', (user_id,))
        return result.fetchone()[0]
    
    def get_id_code(self, phone_num):
        '''Getting a 6dig id code from DB'''
        result = self.cursor.execute('SELECT `user_id` FROM `users` WHERE `phone_num` = ?', (phone_num,))
        return result.fetchone()[0]
    
    def get_phone(self, user_id):
        result = self.cursor.execute('SELECT `phone_num` FROM `users` WHERE `user_id` = ?', (user_id,))
        return result.fetchone()[0]

    def add_nickname(self, nickname, user_id):
        '''Adding user`s TG nickname to DB'''
        self.cursor.execute('INSERT INTO `users` (`nickname`) VAUES (?) WHERE `user_id` = ?', (nickname, user_id))
        return self.connection.commit()
    
    def add_phone_and_code(self, phone_num, code):
        '''Adding into DB users phone and passcode'''
        self.cursor.execute('INSERT INTO `users` (`user_id`, `phone_num`) VALUES (?, ?)', (code, phone_num))
        return self.connection.commit()



    def close(self):
        self.connection.close()





                                 