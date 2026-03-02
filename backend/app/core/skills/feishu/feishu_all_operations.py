"""
飞书全能操作技能包 - 统一入口
支持：文档、表格、多维表格、群聊、日历的完整CRUD操作
"""
import sys
import os
import json
import requests
from datetime import datetime, timezone, timedelta
from typing import Optional, Dict, Any, List

# 添加原skill路径
# sys.path.insert(0, '/workspace/openclaw/skills/feishu-doc-operations/scripts')

# from .feishu_doc_operations import main as doc_main, FeishuDocOperations, obtainIdaasClientId, obtainIdaasClientSecret, obtainUserName
# from .feishu_doc_append import main_doc_append
# from .feishu_sheets_operations import main_sheets
# from .feishu_bitable_operations import main_bitable

def obtainIdaasClientId(): return os.getenv("FEISHU_APP_ID")
def obtainIdaasClientSecret(): return os.getenv("FEISHU_APP_SECRET")
def obtainUserName(): return "jarvis"

def feishu_operation(params):
    """
    飞书统一操作入口
    """
    op_type = params.get('type')
    action = params.get('action')

    # 自动填充认证信息
    if 'client_id' not in params:
        params['client_id'] = obtainIdaasClientId()
    if 'client_secret' not in params:
        params['client_secret'] = obtainIdaasClientSecret()

    try:
        if op_type == 'doc':
            return {"code": -1, "msg": "Doc operations not fully supported in this version (missing dependencies). Use 'drive' for creation."}
            # return _handle_doc(params)
        elif op_type == 'sheet':
            return {"code": -1, "msg": "Sheet operations not fully supported in this version (missing dependencies). Use 'drive' for creation."}
            # return _handle_sheet(params)
        elif op_type == 'bitable':
            return {"code": -1, "msg": "Bitable operations not fully supported in this version (missing dependencies). Use 'drive' for creation."}
            # return _handle_bitable(params)
        elif op_type == 'drive':
            # ... existing logic ...
            pass
        elif op_type == 'card':
            # ... existing logic ...
            pass
        elif op_type == 'chat':
            # ... existing logic ...
            pass
        elif op_type == 'calendar':
            # ... existing logic ...
            pass
        else:
            # Check if it's one of the extended types handled below
            pass

    except Exception as e:
        return {"code": 500, "msg": str(e)}

    # Continue to extended logic
    return _extended_feishu_operation(params)



# def _handle_doc(params):
#     """处理文档操作"""
#     action = params.get('action')

#     if action == 'search':
#         return doc_main({
#             'action': 'search',
#             'keyword': params.get('keyword'),
#             'client_id': params.get('client_id'),
#             'client_secret': params.get('client_secret'),
#             'userName': params.get('userName')
#         })

#     elif action == 'read':
#         return doc_main({
#             'action': 'read',
#             'feishuUrl': params.get('url') or params.get('feishuUrl'),
#             'client_id': params.get('client_id'),
#             'client_secret': params.get('client_secret'),
#             'userName': params.get('userName')
#         })

#     elif action == 'create':
#         return doc_main({
#             'action': 'write',
#             'title': params.get('title'),
#             'content': params.get('content'),
#             'folder_token': params.get('folder_token'),
#             'client_id': params.get('client_id'),
#             'client_secret': params.get('client_secret'),
#             'userName': params.get('userName')
#         })

#     elif action == 'append':
#         return main_doc_append({
#             'action': 'append',
#             'url': params.get('url'),
#             'document_id': params.get('document_id'),
#             'content': params.get('content'),
#             'client_id': params.get('client_id'),
#             'client_secret': params.get('client_secret'),
#             'userName': params.get('userName')
#         })

#     elif action == 'get_blocks':
#         return main_doc_append({
#             'action': 'get_blocks',
#             'url': params.get('url'),
#             'document_id': params.get('document_id'),
#             'client_id': params.get('client_id'),
#             'client_secret': params.get('client_secret'),
#             'userName': params.get('userName')
#         })

#     else:
#         return {"code": -1, "msg": f"不支持的文档操作: {action}"}


# def _handle_sheet(params):
#     """处理表格操作"""
#     action = params.get('action')

#     # 映射action名称
#     action_map = {
#         'create': 'create',
#         'read_meta': 'read_meta',
#         'list_sheets': 'list_sheets',
#         'read_data': 'read_data',
#         'write_data': 'write_data',
#         'append_data': 'append_data',
#         'add_sheet': 'add_sheet'
#     }

#     if action not in action_map:
#         return {"code": -1, "msg": f"不支持的表格操作: {action}"}

#     sheet_params = {
#         'action': action_map[action],
#         'url': params.get('url'),
#         'spreadsheet_token': params.get('spreadsheet_token'),
#         'title': params.get('title'),
#         'sheet_id': params.get('sheet_id'),
#         'range': params.get('range'),
#         'values': params.get('values'),
#         'folder_token': params.get('folder_token'),
#         'client_id': params.get('client_id'),
#         'client_secret': params.get('client_secret'),
#         'userName': params.get('userName')
#     }

#     return main_sheets(sheet_params)


# def _handle_bitable(params):
#     """处理多维表格操作"""
#     action = params.get('action')

#     # 映射action名称
#     action_map = {
#         'create': 'create_bitable',
#         'read_meta': 'read_meta',
#         'list_tables': 'list_tables',
#         'list_fields': 'list_fields',
#         'read_records': 'read_records',
#         'create_table': 'create_table',
#         'create_record': 'create_record',
#         'batch_create_records': 'batch_create_records',
#         'update_record': 'update_record',
#         'delete_record': 'delete_record'
#     }

#     if action not in action_map:
#         return {"code": -1, "msg": f"不支持的多维表格操作: {action}"}

#     bitable_params = {
#         'action': action_map[action],
#         'url': params.get('url'),
#         'app_token': params.get('app_token'),
#         'name': params.get('name'),
#         'table_id': params.get('table_id'),
#         'record_id': params.get('record_id'),
#         'fields': params.get('fields'),
#         'records': params.get('records'),
#         'page_size': params.get('page_size'),
#         'page_token': params.get('page_token'),
#         'folder_token': params.get('folder_token'),
#         'client_id': params.get('client_id'),
#         'client_secret': params.get('client_secret'),
#         'userName': params.get('userName')
#     }

#     return main_bitable(bitable_params)


# CLI入口
if __name__ == "__main__":
    import json
    
    print("飞书全能操作技能包")
    print("=" * 50)
    print("使用方法:")
    print("  from feishu_all_operations import feishu_operation")
    print("  result = feishu_operation({'type': 'doc', 'action': 'read', 'url': '...'})")
    print()
    print("支持的操作类型: doc / sheet / bitable")


# ============================================
# 群共享文件夹和权限管理功能
# ============================================
import requests
import json as json_module


class FeishuDriveOperations:
    """飞书云文档操作类（使用 App Access Token）"""
    
    def __init__(self, app_id: str = None, app_secret: str = None):
        self.app_id = app_id or os.getenv("FEISHU_APP_ID")
        self.app_secret = app_secret or os.getenv("FEISHU_APP_SECRET")
        self.base_url = "https://open.feishu.cn/open-apis"
        self._access_token = None
        self._token_expire_time = 0
    
    def _get_access_token(self) -> str:
        """获取 Tenant Access Token"""
        import time
        
        if self._access_token and time.time() < self._token_expire_time - 300:
            return self._access_token
        
        url = f"{self.base_url}/auth/v3/tenant_access_token/internal"
        response = requests.post(url, json={
            "app_id": self.app_id,
            "app_secret": self.app_secret
        })
        data = response.json()
        
        if data.get("code") != 0:
            raise Exception(f"获取 token 失败: {data}")
        
        self._access_token = data.get("tenant_access_token")
        self._token_expire_time = time.time() + data.get("expire", 7200)
        return self._access_token
    
    def _get_headers(self):
        return {
            "Authorization": f"Bearer {self._get_access_token()}",
            "Content-Type": "application/json"
        }
    
    def get_root_folder_token(self):
        """获取应用根文件夹 token"""
        url = f"{self.base_url}/drive/explorer/v2/root_folder/meta"
        response = requests.get(url, headers=self._get_headers())
        result = response.json()
        
        if result.get("code") == 0:
            return result["data"]["token"]
        return None
    
    def get_root_folder(self):
        """获取应用根文件夹内容"""
        root_token = self.get_root_folder_token()
        if not root_token:
            return {"code": -1, "msg": "无法获取根文件夹"}
        
        url = f"{self.base_url}/drive/v1/files"
        params = {"folder_token": root_token}
        response = requests.get(url, headers=self._get_headers(), params=params)
        return response.json()
    
    def get_chat_shared_folder(self, chat_id: str):
        """
        获取群关联的共享文件夹
        
        逻辑：查找应用根目录下以群ID命名的文件夹，如果没有则创建
        """
        # 1. 获取根目录文件列表
        root_result = self.get_root_folder()
        if root_result.get("code") != 0:
            return root_result
        
        files = root_result.get("data", {}).get("files", [])
        
        # 2. 查找已存在的群共享文件夹
        folder_name = f"群共享_{chat_id[-8:]}"  # 使用群ID后8位作为文件夹名
        
        for f in files:
            if f.get("type") == "folder" and f.get("name") == folder_name:
                return {
                    "code": 0,
                    "msg": "success",
                    "data": {
                        "folder_token": f.get("token"),
                        "folder_name": folder_name,
                        "existed": True
                    }
                }
        
        # 3. 如果不存在，创建新文件夹
        return self.create_folder(folder_name)
    
    def create_folder(self, name: str, parent_token: str = None):
        """创建文件夹"""
        if not parent_token:
            parent_token = self.get_root_folder_token()
        
        url = f"{self.base_url}/drive/v1/files/create_folder"
        data = {
            "name": name,
            "folder_token": parent_token
        }
        
        response = requests.post(url, headers=self._get_headers(), json=data)
        result = response.json()
        
        if result.get("code") == 0:
            return {
                "code": 0,
                "msg": "success",
                "data": {
                    "folder_token": result["data"]["token"],
                    "folder_name": name,
                    "existed": False
                }
            }
        return result
    
    def create_doc_in_folder(self, title: str, folder_token: str, content: str = ""):
        """在指定文件夹中创建文档"""
        url = f"{self.base_url}/docx/v1/documents"
        data = {
            "title": title,
            "folder_token": folder_token
        }
        
        response = requests.post(url, headers=self._get_headers(), json=data)
        result = response.json()
        
        if result.get("code") != 0:
            return result
        
        doc_id = result["data"]["document"]["document_id"]
        doc_url = f"https://li.feishu.cn/docx/{doc_id}"
        
        # 写入内容
        if content:
            content_url = f"{self.base_url}/docx/v1/documents/{doc_id}/blocks/{doc_id}/children"
            content_data = {
                "children": [{
                    "block_type": 2,
                    "text": {
                        "elements": [{
                            "text_run": {"content": content}
                        }]
                    }
                }]
            }
            requests.post(content_url, headers=self._get_headers(), json=content_data)
        
        return {
            "code": 0,
            "msg": "success",
            "data": {
                "document_id": doc_id,
                "url": doc_url,
                "title": title
            }
        }
    
    def add_permission(self, token: str, doc_type: str, member_id: str, 
                      member_type: str = "openid", perm: str = "view",
                      notify: bool = True):
        """
        添加文档权限
        
        Args:
            token: 文档/文件夹 token
            doc_type: 类型 (docx, sheet, bitable, folder)
            member_id: 成员ID (open_id / user_id / email 等)
            member_type: 成员类型 (openid, userid, email, openchat 等)
            perm: 权限 (view, edit, full_access)
            notify: 是否发送通知
        """
        url = f"{self.base_url}/drive/v1/permissions/{token}/members"
        data = {
            "member_type": member_type,
            "member_id": member_id,
            "perm": perm
        }
        params = {
            "type": doc_type,
            "need_notification": "true" if notify else "false"
        }
        
        response = requests.post(url, headers=self._get_headers(), json=data, params=params)
        return response.json()
    
    def add_permissions_batch(self, token: str, doc_type: str, 
                             member_ids: list, perm: str = "view"):
        """批量添加权限"""
        results = []
        for mid in member_ids:
            result = self.add_permission(token, doc_type, mid, perm=perm)
            results.append({
                "member_id": mid,
                "success": result.get("code") == 0,
                "msg": result.get("msg")
            })
        
        success_count = sum(1 for r in results if r["success"])
        return {
            "code": 0 if success_count > 0 else -1,
            "msg": f"成功 {success_count}/{len(member_ids)}",
            "data": {"results": results}
        }
    
    def get_chat_members_ids(self, chat_id: str):
        """获取群成员的 open_id 列表"""
        url = f"{self.base_url}/im/v1/chats/{chat_id}/members"
        params = {"member_id_type": "open_id", "page_size": 100}
        
        response = requests.get(url, headers=self._get_headers(), params=params)
        result = response.json()
        
        if result.get("code") != 0:
            return []
        
        return [m.get("member_id") for m in result.get("data", {}).get("items", [])]
    
    def create_doc_for_chat(self, chat_id: str, title: str, content: str = "",
                           perm: str = "view"):
        """
        在群共享文件夹中创建文档并授权给群成员
        
        这是推荐的一站式方法：
        1. 获取/创建群共享文件夹
        2. 在文件夹中创建文档
        3. 给群成员添加权限
        """
        # 1. 获取群共享文件夹
        folder_result = self.get_chat_shared_folder(chat_id)
        if folder_result.get("code") != 0:
            return folder_result
        
        folder_token = folder_result["data"]["folder_token"]
        
        # 2. 创建文档
        doc_result = self.create_doc_in_folder(title, folder_token, content)
        if doc_result.get("code") != 0:
            return doc_result
        
        doc_id = doc_result["data"]["document_id"]
        
        # 3. 获取群成员
        member_ids = self.get_chat_members_ids(chat_id)
        
        # 4. 添加权限
        perm_result = self.add_permissions_batch(doc_id, "docx", member_ids, perm)
        
        return {
            "code": 0,
            "msg": "success",
            "data": {
                "document_id": doc_id,
                "url": doc_result["data"]["url"],
                "title": title,
                "folder_token": folder_token,
                "permissions": perm_result["data"]
            }
        }
    
    def create_sheet_in_folder(self, title: str, folder_token: str):
        """在指定文件夹中创建表格"""
        url = f"{self.base_url}/sheets/v3/spreadsheets"
        data = {
            "title": title,
            "folder_token": folder_token
        }
        
        response = requests.post(url, headers=self._get_headers(), json=data)
        result = response.json()
        
        if result.get("code") != 0:
            return result
        
        sheet_token = result["data"]["spreadsheet"]["spreadsheet_token"]
        sheet_url = f"https://li.feishu.cn/sheets/{sheet_token}"
        
        return {
            "code": 0,
            "msg": "success",
            "data": {
                "spreadsheet_token": sheet_token,
                "url": sheet_url,
                "title": title
            }
        }
    
    def create_sheet_for_chat(self, chat_id: str, title: str, perm: str = "view"):
        """
        在群共享文件夹中创建表格并授权给群成员
        """
        # 1. 获取群共享文件夹
        folder_result = self.get_chat_shared_folder(chat_id)
        if folder_result.get("code") != 0:
            return folder_result
        
        folder_token = folder_result["data"]["folder_token"]
        
        # 2. 创建表格
        sheet_result = self.create_sheet_in_folder(title, folder_token)
        if sheet_result.get("code") != 0:
            return sheet_result
        
        sheet_token = sheet_result["data"]["spreadsheet_token"]
        
        # 3. 获取群成员并添加权限
        member_ids = self.get_chat_members_ids(chat_id)
        perm_result = self.add_permissions_batch(sheet_token, "sheet", member_ids, perm)
        
        return {
            "code": 0,
            "msg": "success",
            "data": {
                "spreadsheet_token": sheet_token,
                "url": sheet_result["data"]["url"],
                "title": title,
                "folder_token": folder_token,
                "permissions": perm_result["data"]
            }
        }
    
    def create_bitable_in_folder(self, name: str, folder_token: str):
        """在指定文件夹中创建多维表格"""
        url = f"{self.base_url}/bitable/v1/apps"
        data = {
            "name": name,
            "folder_token": folder_token
        }
        
        response = requests.post(url, headers=self._get_headers(), json=data)
        result = response.json()
        
        if result.get("code") != 0:
            return result
        
        app_token = result["data"]["app"]["app_token"]
        bitable_url = f"https://li.feishu.cn/base/{app_token}"
        
        return {
            "code": 0,
            "msg": "success",
            "data": {
                "app_token": app_token,
                "url": bitable_url,
                "name": name
            }
        }
    
    def create_bitable_for_chat(self, chat_id: str, name: str, perm: str = "view"):
        """
        在群共享文件夹中创建多维表格并授权给群成员
        """
        # 1. 获取群共享文件夹
        folder_result = self.get_chat_shared_folder(chat_id)
        if folder_result.get("code") != 0:
            return folder_result
        
        folder_token = folder_result["data"]["folder_token"]
        
        # 2. 创建多维表格
        bitable_result = self.create_bitable_in_folder(name, folder_token)
        if bitable_result.get("code") != 0:
            return bitable_result
        
        app_token = bitable_result["data"]["app_token"]
        
        # 3. 获取群成员并添加权限
        member_ids = self.get_chat_members_ids(chat_id)
        perm_result = self.add_permissions_batch(app_token, "bitable", member_ids, perm)
        
        return {
            "code": 0,
            "msg": "success",
            "data": {
                "app_token": app_token,
                "url": bitable_result["data"]["url"],
                "name": name,
                "folder_token": folder_token,
                "permissions": perm_result["data"]
            }
        }


# 扩展 feishu_operation 函数
_original_feishu_operation = feishu_operation

def feishu_operation(params):
    """
    扩展的统一入口（支持群共享和权限管理）
    
    新增操作 (type='drive'):
        - get_chat_folder: 获取群共享文件夹 (chat_id)
        - create_folder: 创建文件夹 (name, parent_token?)
        - create_doc_for_chat: 在群共享文件夹创建文档并授权 (chat_id, title, content?, perm?)
        - add_permission: 添加权限 (token, doc_type, member_id, perm?)
        - add_permissions_batch: 批量添加权限 (token, doc_type, member_ids, perm?)
    """
    op_type = params.get('type')
    action = params.get('action')
    
    if op_type == 'drive':
        try:
            ops = FeishuDriveOperations()
            
            if action == 'get_chat_folder':
                return ops.get_chat_shared_folder(params.get('chat_id'))
            
            elif action == 'create_folder':
                return ops.create_folder(
                    params.get('name'),
                    params.get('parent_token')
                )
            
            elif action == 'create_doc_for_chat':
                return ops.create_doc_for_chat(
                    chat_id=params.get('chat_id'),
                    title=params.get('title'),
                    content=params.get('content', ''),
                    perm=params.get('perm', 'view')
                )
            
            elif action == 'create_sheet_for_chat':
                return ops.create_sheet_for_chat(
                    chat_id=params.get('chat_id'),
                    title=params.get('title'),
                    perm=params.get('perm', 'view')
                )
            
            elif action == 'create_bitable_for_chat':
                return ops.create_bitable_for_chat(
                    chat_id=params.get('chat_id'),
                    name=params.get('name') or params.get('title'),
                    perm=params.get('perm', 'view')
                )
            
            elif action == 'add_permission':
                return ops.add_permission(
                    token=params.get('token'),
                    doc_type=params.get('doc_type'),
                    member_id=params.get('member_id'),
                    member_type=params.get('member_type', 'openid'),
                    perm=params.get('perm', 'view')
                )
            
            elif action == 'add_permissions_batch':
                return ops.add_permissions_batch(
                    token=params.get('token'),
                    doc_type=params.get('doc_type'),
                    member_ids=params.get('member_ids', []),
                    perm=params.get('perm', 'view')
                )
            
            else:
                return {"code": -1, "msg": f"不支持的 drive 操作: {action}"}
        
        except Exception as e:
            return {"code": -1, "msg": str(e)}
    
    # 卡片消息操作
    elif op_type == 'card':
        try:
            card_ops = FeishuCardOperations()
            
            if action == 'send':
                return card_ops.send_card(
                    receive_id=params.get('receive_id') or params.get('to'),
                    card=params.get('card'),
                    receive_id_type=params.get('receive_id_type', 'open_id')
                )
            
            elif action == 'build':
                return card_ops.build_card(
                    title=params.get('title'),
                    template=params.get('template', 'blue'),
                    elements=params.get('elements', []),
                    content=params.get('content'),
                    fields=params.get('fields'),
                    buttons=params.get('buttons'),
                    note=params.get('note')
                )
            
            elif action == 'build_and_send':
                # 一站式：构建卡片并发送
                # 检查是否有图片
                images = params.get('images')
                if images:
                    card = card_ops.build_card_with_images(
                        title=params.get('title'),
                        template=params.get('template', 'blue'),
                        content=params.get('content'),
                        images=images,
                        fields=params.get('fields'),
                        buttons=params.get('buttons'),
                        note=params.get('note')
                    )
                else:
                    card = card_ops.build_card(
                        title=params.get('title'),
                        template=params.get('template', 'blue'),
                        elements=params.get('elements', []),
                        content=params.get('content'),
                        fields=params.get('fields'),
                        buttons=params.get('buttons'),
                        note=params.get('note')
                    )
                return card_ops.send_card(
                    receive_id=params.get('receive_id') or params.get('to'),
                    card=card,
                    receive_id_type=params.get('receive_id_type', 'open_id')
                )
            
            # 图片处理操作
            elif action == 'upload_image':
                # 上传本地图片到飞书
                image_path = params.get('image_path') or params.get('path')
                if not image_path:
                    return {"code": -1, "msg": "缺少 image_path 参数"}
                image_key = card_ops.upload_image(image_path)
                return {"code": 0, "msg": "success", "data": {"image_key": image_key}}
            
            elif action == 'download_doc_image':
                # 下载飞书文档中的图片
                image_token = params.get('image_token') or params.get('token')
                save_path = params.get('save_path') or params.get('path')
                if not image_token:
                    return {"code": -1, "msg": "缺少 image_token 参数"}
                local_path = card_ops.download_doc_image(image_token, save_path)
                return {"code": 0, "msg": "success", "data": {"path": local_path}}
            
            elif action == 'process_doc_image':
                # 处理单个文档图片：下载 -> 上传 -> 返回 image_key
                image_token = params.get('image_token') or params.get('token')
                cleanup = params.get('cleanup', True)
                if not image_token:
                    return {"code": -1, "msg": "缺少 image_token 参数"}
                image_key = card_ops.process_doc_image(image_token, cleanup)
                return {"code": 0, "msg": "success", "data": {"image_key": image_key, "token": image_token}}
            
            elif action == 'process_doc_images':
                # 批量处理文档图片
                image_tokens = params.get('image_tokens') or params.get('tokens')
                cleanup = params.get('cleanup', True)
                if not image_tokens:
                    return {"code": -1, "msg": "缺少 image_tokens 参数"}
                results = card_ops.process_doc_images(image_tokens, cleanup)
                return {"code": 0, "msg": "success", "data": {"image_keys": results}}
            
            elif action == 'build_with_images':
                # 构建带图片的卡片（不发送）
                card = card_ops.build_card_with_images(
                    title=params.get('title'),
                    template=params.get('template', 'blue'),
                    content=params.get('content'),
                    images=params.get('images'),
                    fields=params.get('fields'),
                    buttons=params.get('buttons'),
                    note=params.get('note')
                )
                return {"code": 0, "msg": "success", "data": {"card": card}}
            
            else:
                return {"code": -1, "msg": f"不支持的 card 操作: {action}，支持: send/build/build_and_send/upload_image/download_doc_image/process_doc_image/process_doc_images/build_with_images"}
        
        except Exception as e:
            return {"code": -1, "msg": str(e)}
    
    # 其他操作走原来的逻辑
    return _original_feishu_operation(params)


# ============================================
# 飞书卡片消息操作
# ============================================

class FeishuCardOperations:
    """飞书卡片消息操作类"""
    
    def __init__(self, app_id: str = None, app_secret: str = None):
        self.app_id = app_id or os.getenv("FEISHU_APP_ID")
        self.app_secret = app_secret or os.getenv("FEISHU_APP_SECRET")
        self.base_url = "https://open.feishu.cn/open-apis"
        self._access_token = None
        self._token_expire_time = 0
    
    def _get_access_token(self) -> str:
        """获取 Tenant Access Token"""
        import time
        
        if self._access_token and time.time() < self._token_expire_time - 300:
            return self._access_token
        
        url = f"{self.base_url}/auth/v3/tenant_access_token/internal"
        response = requests.post(url, json={
            "app_id": self.app_id,
            "app_secret": self.app_secret
        })
        data = response.json()
        
        if data.get("code") != 0:
            raise Exception(f"获取 token 失败: {data}")
        
        self._access_token = data.get("tenant_access_token")
        self._token_expire_time = time.time() + data.get("expire", 7200)
        return self._access_token
    
    def _get_headers(self):
        return {
            "Authorization": f"Bearer {self._get_access_token()}",
            "Content-Type": "application/json"
        }
    
    def build_card(self, title: str, template: str = "blue", elements: list = None,
                   content: str = None, fields: list = None, buttons: list = None,
                   note: str = None) -> dict:
        """
        构建卡片内容
        
        Args:
            title: 卡片标题
            template: 头部颜色模板 (blue/turquoise/green/orange/red/purple/indigo/grey/wathet/yellow/carmine/violet)
            elements: 自定义元素列表（完全自定义时使用）
            content: 正文内容（简单模式）
            fields: 字段列表，每个字段为 {"title": "标题", "value": "内容", "short": True/False}
            buttons: 按钮列表，每个按钮为 {"text": "按钮文本", "url": "跳转链接", "type": "primary/default/danger"}
            note: 底部备注
        
        Returns:
            dict: 卡片内容（可直接用于发送）
        """
        card = {
            "config": {
                "wide_screen_mode": True
            },
            "header": {
                "title": {
                    "tag": "plain_text",
                    "content": title
                },
                "template": template
            },
            "elements": []
        }
        
        # 如果提供了完整的 elements，直接使用
        if elements:
            card["elements"] = elements
            return card
        
        # 简单模式：根据参数构建 elements
        
        # 添加正文内容
        if content:
            card["elements"].append({
                "tag": "div",
                "text": {
                    "tag": "lark_md",
                    "content": content
                }
            })
        
        # 添加字段
        if fields:
            field_elements = []
            for field in fields:
                field_elements.append({
                    "is_short": field.get("short", True),
                    "text": {
                        "tag": "lark_md",
                        "content": f"**{field.get('title', '')}**\n{field.get('value', '')}"
                    }
                })
            
            # 每2个字段一组
            for i in range(0, len(field_elements), 2):
                card["elements"].append({
                    "tag": "div",
                    "fields": field_elements[i:i+2]
                })
        
        # 添加分割线
        if (content or fields) and (buttons or note):
            card["elements"].append({"tag": "hr"})
        
        # 添加按钮
        if buttons:
            actions = []
            for btn in buttons:
                action = {
                    "tag": "button",
                    "text": {
                        "tag": "plain_text",
                        "content": btn.get("text", "按钮")
                    },
                    "type": btn.get("type", "primary")
                }
                if btn.get("url"):
                    action["url"] = btn["url"]
                if btn.get("value"):
                    action["value"] = btn["value"]
                actions.append(action)
            
            card["elements"].append({
                "tag": "action",
                "actions": actions
            })
        
        # 添加底部备注
        if note:
            card["elements"].append({
                "tag": "note",
                "elements": [{
                    "tag": "plain_text",
                    "content": note
                }]
            })
        
        return card
    
    def send_card(self, receive_id: str, card: dict, receive_id_type: str = "open_id") -> dict:
        """
        发送卡片消息
        
        Args:
            receive_id: 接收者ID（open_id/user_id/email/chat_id）
            card: 卡片内容（build_card 返回的字典）
            receive_id_type: ID类型 (open_id/user_id/email/chat_id)
        
        Returns:
            dict: 发送结果
        """
        url = f"{self.base_url}/im/v1/messages"
        params = {"receive_id_type": receive_id_type}
        
        payload = {
            "receive_id": receive_id,
            "msg_type": "interactive",
            "content": json_module.dumps(card)
        }
        
        response = requests.post(url, params=params, headers=self._get_headers(), json=payload)
        result = response.json()
        
        if result.get("code") == 0:
            return {
                "code": 0,
                "msg": "success",
                "data": {
                    "message_id": result["data"]["message_id"],
                    "chat_id": result["data"].get("chat_id")
                }
            }
        else:
            return {
                "code": result.get("code", -1),
                "msg": result.get("msg", "发送失败"),
                "data": result
            }
    
    def send_simple_card(self, receive_id: str, title: str, content: str,
                        template: str = "blue", note: str = None,
                        receive_id_type: str = "open_id") -> dict:
        """
        发送简单卡片（快捷方法）
        
        Args:
            receive_id: 接收者ID
            title: 标题
            content: 正文内容（支持 Markdown）
            template: 颜色模板
            note: 底部备注
            receive_id_type: ID类型
        """
        card = self.build_card(
            title=title,
            template=template,
            content=content,
            note=note
        )
        return self.send_card(receive_id, card, receive_id_type)
    
    # ============================================
    # 图片处理功能
    # ============================================
    
    def _get_user_token(self) -> str:
        """
        获取用户飞书访问令牌（用于下载文档中的图片）
        
        Returns:
            str: 用户访问令牌
        """
        import asyncio
        from idaas.app import TokenManager
        
        # 配置
        host = "https://cfe-feishu-server.chehejia.com"
        endpoint = "https://id.lixiang.com/api"
        feishu_appid = "cli_a9bc3a82cef9dbd3"
        service_id = "35CWIoLZyI9uyZlJ6ASkAc"
        client_id = obtainIdaasClientId()
        client_secret = obtainIdaasClientSecret()
        user_name = obtainUserName()
        scopes = ["doc:write", "doc:read", "default"]
        
        # 获取服务 token
        manager = TokenManager.singleton_m2m(endpoint, client_id, lambda cli: client_secret)
        bundle = asyncio.run(manager.get_token(client_id, service_id, *scopes))
        service_token = bundle.access_token
        
        # 获取用户飞书 token
        auth_url = f"{host}/api/auth/token?clientId={feishu_appid}&userName={user_name}"
        headers = {
            "x-feishu-appid": feishu_appid,
            "Authorization": f"Bearer {service_token}",
        }
        resp = requests.get(auth_url, headers=headers)
        auth_data = resp.json()
        
        if auth_data.get('code') != 0:
            raise Exception(f"获取用户 token 失败: {auth_data}")
        
        return auth_data.get('data', {}).get('accessToken')
    
    def download_doc_image(self, image_token: str, save_path: str = None) -> str:
        """
        下载飞书文档中的图片
        
        Args:
            image_token: 图片 token（从文档块中获取）
            save_path: 保存路径，默认保存到临时目录
        
        Returns:
            str: 图片保存路径
        """
        import tempfile
        
        user_token = self._get_user_token()
        
        url = f"https://open.feishu.cn/open-apis/drive/v1/medias/{image_token}/download"
        headers = {"Authorization": f"Bearer {user_token}"}
        
        resp = requests.get(url, headers=headers, timeout=60)
        
        if resp.status_code != 200 or 'image' not in resp.headers.get('Content-Type', ''):
            raise Exception(f"下载图片失败: {resp.status_code}, {resp.text[:200]}")
        
        # 确定文件扩展名
        content_type = resp.headers.get('Content-Type', 'image/png')
        ext = content_type.split('/')[-1]
        if ext not in ['png', 'jpg', 'jpeg', 'gif', 'webp']:
            ext = 'png'
        
        # 保存路径
        if not save_path:
            temp_dir = tempfile.mkdtemp(prefix='feishu_images_')
            save_path = os.path.join(temp_dir, f"{image_token}.{ext}")
        
        with open(save_path, 'wb') as f:
            f.write(resp.content)
        
        return save_path
    
    def upload_image(self, image_path: str) -> str:
        """
        上传图片到飞书消息系统
        
        Args:
            image_path: 本地图片路径
        
        Returns:
            str: image_key（用于在卡片中引用）
        """
        url = f"{self.base_url}/im/v1/images"
        
        # 确定 MIME 类型
        ext = os.path.splitext(image_path)[1].lower()
        mime_types = {
            '.png': 'image/png',
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.gif': 'image/gif',
            '.webp': 'image/webp'
        }
        mime_type = mime_types.get(ext, 'image/png')
        
        with open(image_path, 'rb') as f:
            files = {
                'image': (os.path.basename(image_path), f, mime_type)
            }
            data = {'image_type': 'message'}
            headers = {'Authorization': f'Bearer {self._get_access_token()}'}
            
            resp = requests.post(url, headers=headers, files=files, data=data, timeout=120)
        
        if resp.status_code != 200:
            raise Exception(f"上传图片失败: {resp.status_code}, {resp.text[:200]}")
        
        result = resp.json()
        if result.get('code') != 0:
            raise Exception(f"上传图片失败: {result}")
        
        return result.get('data', {}).get('image_key')
    
    def process_doc_image(self, image_token: str, cleanup: bool = True) -> str:
        """
        处理飞书文档图片：下载 -> 上传 -> 返回 image_key
        
        Args:
            image_token: 文档中的图片 token
            cleanup: 是否在上传后删除临时文件
        
        Returns:
            str: image_key（用于在卡片中引用）
        """
        import shutil
        
        # 下载
        local_path = self.download_doc_image(image_token)
        temp_dir = os.path.dirname(local_path)
        
        try:
            # 上传
            image_key = self.upload_image(local_path)
            return image_key
        finally:
            # 清理
            if cleanup and temp_dir and temp_dir.startswith('/tmp'):
                shutil.rmtree(temp_dir, ignore_errors=True)
    
    def process_doc_images(self, image_tokens: list, cleanup: bool = True) -> dict:
        """
        批量处理飞书文档图片
        
        Args:
            image_tokens: 图片 token 列表，可以是字符串列表或 {"token": "xxx", "name": "描述"} 列表
            cleanup: 是否在上传后删除临时文件
        
        Returns:
            dict: {token: image_key} 或 {name: image_key} 映射
        """
        import tempfile
        import shutil
        
        temp_dir = tempfile.mkdtemp(prefix='feishu_images_')
        results = {}
        
        try:
            user_token = self._get_user_token()
            download_headers = {"Authorization": f"Bearer {user_token}"}
            
            # 下载所有图片
            downloaded = []
            for item in image_tokens:
                if isinstance(item, str):
                    token = item
                    name = token
                else:
                    token = item.get('token')
                    name = item.get('name', token)
                
                url = f"https://open.feishu.cn/open-apis/drive/v1/medias/{token}/download"
                resp = requests.get(url, headers=download_headers, timeout=60)
                
                if resp.status_code == 200 and 'image' in resp.headers.get('Content-Type', ''):
                    ext = resp.headers.get('Content-Type', 'image/png').split('/')[-1]
                    if ext not in ['png', 'jpg', 'jpeg', 'gif', 'webp']:
                        ext = 'png'
                    local_path = os.path.join(temp_dir, f"{token}.{ext}")
                    with open(local_path, 'wb') as f:
                        f.write(resp.content)
                    downloaded.append((name, local_path))
            
            # 上传所有图片
            for name, local_path in downloaded:
                try:
                    image_key = self.upload_image(local_path)
                    results[name] = image_key
                except Exception as e:
                    results[name] = f"ERROR: {e}"
            
            return results
        finally:
            # 清理
            if cleanup:
                shutil.rmtree(temp_dir, ignore_errors=True)
    
    def build_card_with_images(self, title: str, template: str = "blue",
                               content: str = None, images: list = None,
                               fields: list = None, buttons: list = None,
                               note: str = None) -> dict:
        """
        构建带图片的卡片
        
        Args:
            title: 卡片标题
            template: 颜色模板
            content: 正文内容
            images: 图片列表，每个元素为 {"image_key": "xxx", "alt": "描述"} 或直接是 image_key 字符串
            fields: 字段列表
            buttons: 按钮列表
            note: 底部备注
        
        Returns:
            dict: 卡片内容
        """
        card = {
            "config": {"wide_screen_mode": True},
            "header": {
                "title": {"tag": "plain_text", "content": title},
                "template": template
            },
            "elements": []
        }
        
        # 添加正文
        if content:
            card["elements"].append({
                "tag": "div",
                "text": {"tag": "lark_md", "content": content}
            })
        
        # 添加图片
        if images:
            for img in images:
                if isinstance(img, str):
                    img_key = img
                    alt_text = "图片"
                else:
                    img_key = img.get('image_key')
                    alt_text = img.get('alt', '图片')
                
                card["elements"].append({
                    "tag": "img",
                    "img_key": img_key,
                    "alt": {"tag": "plain_text", "content": alt_text}
                })
        
        # 添加字段
        if fields:
            field_elements = []
            for field in fields:
                field_elements.append({
                    "is_short": field.get("short", True),
                    "text": {
                        "tag": "lark_md",
                        "content": f"**{field.get('title', '')}**\n{field.get('value', '')}"
                    }
                })
            for i in range(0, len(field_elements), 2):
                card["elements"].append({
                    "tag": "div",
                    "fields": field_elements[i:i+2]
                })
        
        # 分割线
        if (content or images or fields) and (buttons or note):
            card["elements"].append({"tag": "hr"})
        
        # 按钮
        if buttons:
            actions = []
            for btn in buttons:
                action = {
                    "tag": "button",
                    "text": {"tag": "plain_text", "content": btn.get("text", "按钮")},
                    "type": btn.get("type", "primary")
                }
                if btn.get("url"):
                    action["url"] = btn["url"]
                actions.append(action)
            card["elements"].append({"tag": "action", "actions": actions})
        
        # 备注
        if note:
            card["elements"].append({
                "tag": "note",
                "elements": [{"tag": "plain_text", "content": note}]
            })
        
        return card


# ============================================
# 飞书群聊操作
# ============================================

class FeishuChatOperations:
    """飞书群聊操作类"""
    
    def __init__(self, app_id: str = None, app_secret: str = None):
        self.app_id = app_id or os.getenv("FEISHU_APP_ID")
        self.app_secret = app_secret or os.getenv("FEISHU_APP_SECRET")
        self.base_url = "https://open.feishu.cn/open-apis"
        self._access_token = None
        self._token_expire_time = 0
        
        if not self.app_id or not self.app_secret:
            raise ValueError("Missing FEISHU_APP_ID or FEISHU_APP_SECRET")
    
    def _get_access_token(self) -> str:
        """获取 App Access Token（带缓存）"""
        import time
        
        if self._access_token and time.time() < self._token_expire_time - 300:
            return self._access_token
        
        url = f"{self.base_url}/auth/v3/app_access_token/internal"
        payload = {
            "app_id": self.app_id,
            "app_secret": self.app_secret
        }
        
        response = requests.post(url, json=payload)
        data = response.json()
        
        if data.get("code") != 0:
            raise Exception(f"获取 token 失败: {data}")
        
        self._access_token = data.get("app_access_token")
        self._token_expire_time = time.time() + data.get("expire", 7200)
        
        return self._access_token
    
    def _get_headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self._get_access_token()}",
            "Content-Type": "application/json; charset=utf-8"
        }
    
    def list_chats(self, page_size: int = 100, page_token: str = None) -> Dict[str, Any]:
        """获取机器人所在的所有群列表"""
        url = f"{self.base_url}/im/v1/chats"
        params = {"page_size": page_size}
        if page_token:
            params["page_token"] = page_token
        
        response = requests.get(url, headers=self._get_headers(), params=params)
        return response.json()
    
    def search_chat(self, keyword: str) -> Dict[str, Any]:
        """按名称搜索群聊"""
        all_chats = []
        page_token = None
        
        while True:
            result = self.list_chats(page_size=100, page_token=page_token)
            if result.get("code") != 0:
                return result
            
            items = result.get("data", {}).get("items", [])
            all_chats.extend(items)
            
            page_token = result.get("data", {}).get("page_token")
            if not page_token or not result.get("data", {}).get("has_more"):
                break
        
        matched = []
        for chat in all_chats:
            name = chat.get("name", "")
            if keyword.lower() in name.lower():
                matched.append({
                    "name": name,
                    "chat_id": chat.get("chat_id"),
                    "owner_id": chat.get("owner_id"),
                    "chat_mode": chat.get("chat_mode"),
                    "avatar": chat.get("avatar")
                })
        
        return {"code": 0, "msg": "success", "data": {"chats": matched, "total": len(matched)}}
    
    def get_chat_info(self, chat_id: str) -> Dict[str, Any]:
        """获取群聊基本信息"""
        url = f"{self.base_url}/im/v1/chats/{chat_id}"
        response = requests.get(url, headers=self._get_headers())
        return response.json()
    
    def get_chat_members(self, chat_id: str, page_size: int = 100, page_token: str = None) -> Dict[str, Any]:
        """获取群成员列表"""
        url = f"{self.base_url}/im/v1/chats/{chat_id}/members"
        params = {"member_id_type": "open_id", "page_size": page_size}
        if page_token:
            params["page_token"] = page_token
        
        response = requests.get(url, headers=self._get_headers(), params=params)
        return response.json()
    
    def get_user_info(self, user_id: str, id_type: str = "open_id") -> Dict[str, Any]:
        """获取单个用户详细信息"""
        url = f"{self.base_url}/contact/v3/users/{user_id}"
        params = {"user_id_type": id_type}
        response = requests.get(url, headers=self._get_headers(), params=params)
        return response.json()
    
    def get_users_batch(self, user_ids: List[str], id_type: str = "open_id") -> Dict[str, Any]:
        """批量获取用户信息"""
        url = f"{self.base_url}/contact/v3/users/batch"
        param_list = [("user_id_type", id_type)]
        for uid in user_ids:
            param_list.append(("user_ids", uid))
        
        response = requests.get(url, headers=self._get_headers(), params=param_list)
        return response.json()
    
    def get_chat_history(self, chat_id: str, page_size: int = 50, page_token: str = None,
                         start_time: str = None, end_time: str = None) -> Dict[str, Any]:
        """获取群聊历史消息"""
        url = f"{self.base_url}/im/v1/messages"
        params = {
            "container_id_type": "chat",
            "container_id": chat_id,
            "page_size": page_size,
            "sort_type": "ByCreateTimeDesc"
        }
        
        if page_token:
            params["page_token"] = page_token
        if start_time:
            params["start_time"] = start_time
        if end_time:
            params["end_time"] = end_time
        
        response = requests.get(url, headers=self._get_headers(), params=params)
        return response.json()
    
    def get_members_with_details(self, chat_id: str) -> Dict[str, Any]:
        """获取群成员及其详细信息"""
        members_result = self.get_chat_members(chat_id)
        if members_result.get("code") != 0:
            return members_result
        
        items = members_result.get("data", {}).get("items", [])
        if not items:
            return {"code": 0, "msg": "success", "data": {"members": []}}
        
        open_ids = [m.get("member_id") for m in items if m.get("member_id")]
        users_result = self.get_users_batch(open_ids)
        
        if users_result.get("code") != 0:
            return {"code": 0, "msg": "success", "data": {"members": items, "details_error": users_result.get("msg")}}
        
        user_details = {u.get("open_id"): u for u in users_result.get("data", {}).get("items", [])}
        
        enriched_members = []
        for m in items:
            member_id = m.get("member_id")
            detail = user_details.get(member_id, {})
            enriched_members.append({
                "name": m.get("name"),
                "member_id": member_id,
                "email": detail.get("email") or detail.get("enterprise_email"),
                "mobile": detail.get("mobile"),
                "en_name": detail.get("en_name"),
                "employee_no": detail.get("employee_no"),
                "job_title": self._extract_job_title(detail),
                "department_ids": detail.get("department_ids", []),
                "avatar": detail.get("avatar", {}).get("avatar_72"),
                "status": detail.get("status", {}),
                "full_detail": detail
            })
        
        return {"code": 0, "msg": "success", "data": {"members": enriched_members, "total": len(enriched_members)}}
    
    def _extract_job_title(self, user_detail: Dict) -> str:
        """从用户详情中提取职位信息"""
        custom_attrs = user_detail.get("custom_attrs", [])
        for attr in custom_attrs:
            attr_id = attr.get("id", "")
            if "7215564902148046849" in attr_id:
                return attr.get("value", {}).get("text", "")
        return user_detail.get("job_title", "")
    
    def format_messages(self, messages: List[Dict]) -> List[Dict]:
        """格式化消息列表为易读格式"""
        formatted = []
        for msg in messages:
            msg_type = msg.get("msg_type", "unknown")
            sender = msg.get("sender", {})
            
            create_time = msg.get("create_time", "0")
            try:
                dt = datetime.fromtimestamp(int(create_time) / 1000)
                time_str = dt.strftime("%Y-%m-%d %H:%M:%S")
            except:
                time_str = create_time
            
            body = msg.get("body", {})
            content = body.get("content", "{}")
            
            try:
                content_obj = json.loads(content)
                if msg_type == "text":
                    text = content_obj.get("text", content)
                elif msg_type == "post":
                    text = f"[富文本] {content_obj.get('title', '')}"
                elif msg_type == "image":
                    text = "[图片]"
                elif msg_type == "file":
                    text = f"[文件] {content_obj.get('file_name', '')}"
                elif msg_type == "sticker":
                    text = "[表情]"
                elif msg_type == "interactive":
                    text = "[卡片消息]"
                elif msg_type == "share_chat":
                    text = "[分享群聊]"
                else:
                    text = f"[{msg_type}]"
            except:
                text = content[:200] if content else "(empty)"
            
            formatted.append({
                "time": time_str,
                "sender_type": sender.get("sender_type"),
                "sender_id": sender.get("id"),
                "msg_type": msg_type,
                "text": text,
                "message_id": msg.get("message_id")
            })
        
        return formatted


# ============================================
# 飞书日历操作
# ============================================

class FeishuCalendarOperations(FeishuChatOperations):
    """飞书日历操作类（继承自 FeishuChatOperations）"""
    
    def __init__(self, app_id: str = None, app_secret: str = None):
        super().__init__(app_id, app_secret)
        self._calendar_id = None
    
    def get_calendar_id(self) -> str:
        """获取应用的主日历 ID"""
        if self._calendar_id:
            return self._calendar_id
        
        url = f"{self.base_url}/calendar/v4/calendars"
        response = requests.get(url, headers=self._get_headers())
        result = response.json()
        
        if result.get("code") == 0:
            calendars = result.get("data", {}).get("calendar_list", [])
            for cal in calendars:
                if cal.get("type") == "primary":
                    self._calendar_id = cal.get("calendar_id")
                    return self._calendar_id
        
        raise Exception(f"获取日历失败: {result}")
    
    def get_user_freebusy(self, user_id: str, time_min: str, time_max: str) -> Dict[str, Any]:
        """查询用户的忙闲状态"""
        url = f"{self.base_url}/calendar/v4/freebusy/list"
        data = {"time_min": time_min, "time_max": time_max, "user_id": user_id}
        
        response = requests.post(url, headers=self._get_headers(), json=data, 
                                params={"user_id_type": "open_id"})
        return response.json()
    
    def find_free_slots(self, user_ids: List[str], date: str, 
                        start_hour: int = 9, end_hour: int = 18,
                        duration_minutes: int = 30) -> List[Dict]:
        """查找多个用户的共同空闲时段"""
        tz = timezone(timedelta(hours=8))
        
        time_min = f"{date}T{start_hour:02d}:00:00+08:00"
        time_max = f"{date}T{end_hour:02d}:00:00+08:00"
        
        all_busy = []
        for user_id in user_ids:
            result = self.get_user_freebusy(user_id, time_min, time_max)
            if result.get("code") == 0:
                for item in result.get("data", {}).get("freebusy_list", []):
                    start = item.get("start_time")
                    end = item.get("end_time")
                    all_busy.append((start, end))
        
        def time_to_minutes(t: str) -> int:
            hour = int(t[11:13])
            minute = int(t[14:16])
            return hour * 60 + minute
        
        busy_intervals = []
        for start, end in all_busy:
            busy_intervals.append((time_to_minutes(start), time_to_minutes(end)))
        
        busy_intervals.sort()
        merged = []
        for start, end in busy_intervals:
            if merged and start <= merged[-1][1]:
                merged[-1] = (merged[-1][0], max(merged[-1][1], end))
            else:
                merged.append((start, end))
        
        free_slots = []
        current = start_hour * 60
        end_minutes = end_hour * 60
        
        for busy_start, busy_end in merged:
            if current < busy_start:
                gap = busy_start - current
                if gap >= duration_minutes:
                    free_slots.append({
                        "start": f"{current // 60:02d}:{current % 60:02d}",
                        "end": f"{busy_start // 60:02d}:{busy_start % 60:02d}",
                        "duration": gap
                    })
            current = max(current, busy_end)
        
        if current < end_minutes:
            gap = end_minutes - current
            if gap >= duration_minutes:
                free_slots.append({
                    "start": f"{current // 60:02d}:{current % 60:02d}",
                    "end": f"{end_minutes // 60:02d}:{end_minutes % 60:02d}",
                    "duration": gap
                })
        
        return free_slots
    
    def create_event(self, summary: str, start_time: str, end_time: str,
                     attendee_ids: List[str] = None, description: str = "",
                     with_video: bool = True) -> Dict[str, Any]:
        """创建日程/会议"""
        calendar_id = self.get_calendar_id()
        url = f"{self.base_url}/calendar/v4/calendars/{calendar_id}/events"
        
        event_data = {
            "summary": summary,
            "description": description,
            "need_notification": True,
            "start_time": {"timestamp": str(start_time)},
            "end_time": {"timestamp": str(end_time)},
            "visibility": "default",
            "attendee_ability": "can_modify_event",
            "free_busy_status": "busy"
        }
        
        if with_video:
            event_data["vchat"] = {"vc_type": "vc"}
        
        response = requests.post(url, headers=self._get_headers(), json=event_data,
                                params={"user_id_type": "open_id"})
        result = response.json()
        
        if result.get("code") == 0 and attendee_ids:
            event_id = result["data"]["event"]["event_id"]
            self.add_attendees(calendar_id, event_id, attendee_ids)
        
        return result
    
    def add_attendees(self, calendar_id: str, event_id: str, user_ids: List[str]) -> Dict[str, Any]:
        """添加参会人"""
        url = f"{self.base_url}/calendar/v4/calendars/{calendar_id}/events/{event_id}/attendees"
        data = {
            "attendees": [{"type": "user", "user_id": uid} for uid in user_ids],
            "need_notification": True
        }
        
        response = requests.post(url, headers=self._get_headers(), json=data,
                                params={"user_id_type": "open_id"})
        return response.json()
    
    def update_event(self, event_id: str, **kwargs) -> Dict[str, Any]:
        """更新日程"""
        calendar_id = self.get_calendar_id()
        url = f"{self.base_url}/calendar/v4/calendars/{calendar_id}/events/{event_id}"
        
        response = requests.patch(url, headers=self._get_headers(), json=kwargs)
        return response.json()
    
    def schedule_meeting_for_chat(self, chat_id: str, summary: str,
                                  date: str, prefer_afternoon: bool = True,
                                  duration_minutes: int = 30) -> Dict[str, Any]:
        """为群聊成员智能安排会议"""
        members_result = self.get_chat_members(chat_id)
        if members_result.get("code") != 0:
            return members_result
        
        user_ids = [m["member_id"] for m in members_result.get("data", {}).get("items", [])]
        
        if not user_ids:
            return {"code": -1, "msg": "群内没有成员"}
        
        start_hour = 14 if prefer_afternoon else 9
        end_hour = 18
        
        free_slots = self.find_free_slots(user_ids, date, start_hour, end_hour, duration_minutes)
        
        if not free_slots and prefer_afternoon:
            free_slots = self.find_free_slots(user_ids, date, 9, 12, duration_minutes)
        
        if not free_slots:
            return {"code": -1, "msg": f"在 {date} 找不到所有人都空闲的时段"}
        
        slot = free_slots[0]
        
        tz = timezone(timedelta(hours=8))
        start_dt = datetime.strptime(f"{date} {slot['start']}", "%Y-%m-%d %H:%M")
        start_dt = start_dt.replace(tzinfo=tz)
        end_dt = start_dt + timedelta(minutes=duration_minutes)
        
        start_ts = int(start_dt.timestamp())
        end_ts = int(end_dt.timestamp())
        
        result = self.create_event(
            summary=summary,
            start_time=start_ts,
            end_time=end_ts,
            attendee_ids=user_ids,
            description=f"由硅基人自动安排\n参会人: {len(user_ids)} 人",
            with_video=True
        )
        
        if result.get("code") == 0:
            result["scheduled_time"] = {
                "date": date,
                "start": slot["start"],
                "end": f"{end_dt.hour:02d}:{end_dt.minute:02d}",
                "free_slots_found": free_slots
            }
        
        return result


# ============================================
# 扩展统一入口：支持 chat 和 calendar
# ============================================

_extended_feishu_operation = feishu_operation

def feishu_operation(params):
    """
    扩展的统一入口（支持群聊和日历操作）
    
    群聊操作 (type='chat'):
        - list_chats: 列出所有群
        - search_chat: 搜索群聊 (keyword)
        - get_chat_info: 获取群信息 (chat_id)
        - get_members: 获取群成员 (chat_id)
        - get_members_detail: 获取群成员详情 (chat_id)
        - get_history: 获取聊天记录 (chat_id, page_size?, format?)
        - get_user_info: 获取用户信息 (user_id)
    
    日历操作 (type='calendar'):
        - get_freebusy: 查询忙闲 (user_id, time_min, time_max)
        - find_free_slots: 查找空闲时段 (user_ids, date, start_hour?, end_hour?, duration_minutes?)
        - create_event: 创建日程 (summary, start_time, end_time, attendee_ids?, with_video?)
        - update_event: 更新日程 (event_id, ...)
        - schedule_meeting: 智能约会 (chat_id, summary, date, prefer_afternoon?, duration_minutes?)
    """
    op_type = params.get('type')
    action = params.get('action')
    
    # 群聊操作
    if op_type == 'chat':
        try:
            ops = FeishuChatOperations()
            
            if action == 'list_chats':
                return ops.list_chats(
                    page_size=params.get('page_size', 100),
                    page_token=params.get('page_token')
                )
            
            elif action == 'search_chat':
                return ops.search_chat(params.get('keyword', ''))
            
            elif action == 'get_chat_info':
                return ops.get_chat_info(params.get('chat_id'))
            
            elif action == 'get_members':
                return ops.get_chat_members(
                    params.get('chat_id'),
                    page_size=params.get('page_size', 100),
                    page_token=params.get('page_token')
                )
            
            elif action == 'get_members_detail':
                return ops.get_members_with_details(params.get('chat_id'))
            
            elif action == 'get_user_info':
                return ops.get_user_info(
                    params.get('user_id'),
                    id_type=params.get('id_type', 'open_id')
                )
            
            elif action == 'get_history':
                result = ops.get_chat_history(
                    params.get('chat_id'),
                    page_size=params.get('page_size', 50),
                    page_token=params.get('page_token'),
                    start_time=params.get('start_time'),
                    end_time=params.get('end_time')
                )
                
                if params.get('format') and result.get("code") == 0:
                    items = result.get("data", {}).get("items", [])
                    result["data"]["formatted"] = ops.format_messages(items)
                
                return result
            
            else:
                return {"code": -1, "msg": f"不支持的 chat 操作: {action}"}
        
        except Exception as e:
            return {"code": -1, "msg": str(e)}
    
    # 日历操作
    elif op_type == 'calendar':
        try:
            ops = FeishuCalendarOperations()
            
            if action == 'get_freebusy':
                return ops.get_user_freebusy(
                    params.get('user_id'),
                    params.get('time_min'),
                    params.get('time_max')
                )
            
            elif action == 'find_free_slots':
                slots = ops.find_free_slots(
                    params.get('user_ids', []),
                    params.get('date'),
                    params.get('start_hour', 9),
                    params.get('end_hour', 18),
                    params.get('duration_minutes', 30)
                )
                return {"code": 0, "msg": "success", "data": {"free_slots": slots}}
            
            elif action == 'create_event':
                return ops.create_event(
                    summary=params.get('summary'),
                    start_time=params.get('start_time'),
                    end_time=params.get('end_time'),
                    attendee_ids=params.get('attendee_ids', []),
                    description=params.get('description', ''),
                    with_video=params.get('with_video', True)
                )
            
            elif action == 'update_event':
                update_fields = {k: v for k, v in params.items() 
                               if k not in ['type', 'action', 'event_id']}
                return ops.update_event(params.get('event_id'), **update_fields)
            
            elif action == 'schedule_meeting':
                return ops.schedule_meeting_for_chat(
                    chat_id=params.get('chat_id'),
                    summary=params.get('summary'),
                    date=params.get('date'),
                    prefer_afternoon=params.get('prefer_afternoon', True),
                    duration_minutes=params.get('duration_minutes', 30)
                )
            
            else:
                return {"code": -1, "msg": f"不支持的 calendar 操作: {action}"}
        
        except Exception as e:
            return {"code": -1, "msg": str(e)}
    
    # 其他操作走原来的逻辑
    return _extended_feishu_operation(params)
