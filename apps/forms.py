class FormMixin:
    def get_error(self):
        if hasattr(self, 'errors'):
            # <ul class="errorlist"><li>telephone<ul class="errorlist"><li>长度有误</li></ul></li></ul>
            # API 文档 是后端写的  直接自己写
            # {"telephone":"长度有"}
            #  json as_p as_ul
            """
            {
                'telephone': [
                    {'message': '手机号长度有误', 'code': 'min_length'}
                ],
                'password': [
                    {'message': '密码长度有误', 'code': 'min_length'}
                ]
            }
            """
            # json格式的数据
            error_json = self.errors.get_json_data()
            # ('telephone', [{'message': '手机号长度有误', 'code': 'min_length'}])
            error_tuple = error_json.popitem()
            #  [{'message': '手机号长度有误', 'code': 'min_length'}]
            error_list = error_tuple[1]
            error_dict = error_list[0]
            # print(error_list)
            # print(error_dict["message"])
            message = error_dict["message"]
            return message
            # print(dir(form.errors))
            # print(error_json)
        return None
