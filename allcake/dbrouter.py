class MultiDBRouter(object):
    def __init__(self):
        self.model_list = {}
    def db_for_read(self, model, **hints):
        """
        chatdb 앱의 모델을 조회하는 경우 chat_db로 중계한다.
        """
        if model._meta.app_label in self.model_list:
            return 'chat_db'
        return None

    def db_for_wirte(self, model, **hints):
        """
        chat 앱의 모델을 기록하는 경우 chat_db 중계한다.
        """
        if model._meta.app_label in self.model_list:
            return 'chat_db'
        return None
    
    def allow_relation(self, obj1, obj2, **hints):
        """
        chat 앱의 모델과 관련된 관계 접근을 허용한다.
        """
        if (
            obj1._meta.app_label in self.model_list or
            obj2._meta.app_label in self.model_list
        ):
            return True
        return None
    
    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        chatdb 앱의 모델에 대응하는 표가 chat_db 데이터베이스에만 생성되도록 한다.
        """
        if db =='chat_db':
            if app_label in self.model_list:
                print(db, app_label, model_name, "TRUE")
                return True
            else:
                print(db, app_label, model_name, "FALSE")
                return False
        print(db, app_label, model_name, "NONE")
        return None