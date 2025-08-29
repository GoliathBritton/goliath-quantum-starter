#!/usr/bin/env python3
"""
🔐 Role-Based Access Control (RBAC)

Implements granular permission management and access control
for the NQBA ecosystem with hierarchical role structure.
"""

from typing import Dict, List, Set, Optional
from .models import Role, Permission, RoleLevel, PermissionCategory
from datetime import datetime

class RoleBasedAccessControl:
    """Role-based access control system"""
    
    def __init__(self):
        self.roles: Dict[str, Role] = {}
        self.permissions: Dict[str, Permission] = {}
        self.role_hierarchy: Dict[RoleLevel, List[RoleLevel]] = {
            RoleLevel.FOUNDER: [RoleLevel.EXECUTIVE, RoleLevel.ARCHITECT, RoleLevel.ADMIN, RoleLevel.MANAGER, RoleLevel.USER, RoleLevel.GUEST],
            RoleLevel.EXECUTIVE: [RoleLevel.ARCHITECT, RoleLevel.ADMIN, RoleLevel.MANAGER, RoleLevel.USER, RoleLevel.GUEST],
            RoleLevel.ARCHITECT: [RoleLevel.ADMIN, RoleLevel.MANAGER, RoleLevel.USER, RoleLevel.GUEST],
            RoleLevel.ADMIN: [RoleLevel.MANAGER, RoleLevel.USER, RoleLevel.GUEST],
            RoleLevel.MANAGER: [RoleLevel.USER, RoleLevel.GUEST],
            RoleLevel.USER: [RoleLevel.GUEST],
            RoleLevel.GUEST: []
        }
        self._initialize_system_roles()
    
    def _initialize_system_roles(self):
        """Initialize system roles with default permissions"""
        
        # Create system permissions
        system_permissions = [
            Permission(
                name="system_admin",
                category=PermissionCategory.SYSTEM,
                description="Full system administration access",
                resource="system",
                action="all"
            ),
            Permission(
                name="user_manage",
                category=PermissionCategory.USER,
                description="Manage all users",
                resource="users",
                action="all"
            ),
            Permission(
                name="role_manage",
                category=PermissionCategory.USER,
                description="Manage roles and permissions",
                resource="roles",
                action="all"
            ),
            Permission(
                name="business_manage",
                category=PermissionCategory.BUSINESS,
                description="Manage business units",
                resource="business_units",
                action="all"
            ),
            Permission(
                name="ecosystem_manage",
                category=PermissionCategory.ECOSYSTEM,
                description="Manage ecosystem layers",
                resource="ecosystem",
                action="all"
            ),
            Permission(
                name="quantum_access",
                category=PermissionCategory.QUANTUM,
                description="Access quantum operations",
                resource="quantum",
                action="read"
            ),
            Permission(
                name="data_access",
                category=PermissionCategory.DATA,
                description="Access system data",
                resource="data",
                action="read"
            ),
            Permission(
                name="financial_access",
                category=PermissionCategory.FINANCIAL,
                description="Access financial operations",
                resource="financial",
                action="read"
            )
        ]
        
        # Add permissions to the system
        for perm in system_permissions:
            self.permissions[perm.id] = perm
        
        # Create system roles
        founder_role = Role(
            name="Founder",
            level=RoleLevel.FOUNDER,
            description="Absolute control over the entire NQBA ecosystem",
            permissions=[perm.id for perm in system_permissions],
            is_system_role=True
        )
        
        executive_role = Role(
            name="Executive",
            level=RoleLevel.EXECUTIVE,
            description="High council member with strategic oversight",
            permissions=[perm.id for perm in system_permissions if perm.category != PermissionCategory.SYSTEM],
            is_system_role=True
        )
        
        architect_role = Role(
            name="Architect",
            level=RoleLevel.ARCHITECT,
            description="Technical architect with system design authority",
            permissions=[
                perm.id for perm in system_permissions 
                if perm.category in [PermissionCategory.BUSINESS, PermissionCategory.ECOSYSTEM, PermissionCategory.QUANTUM]
            ],
            is_system_role=True
        )
        
        admin_role = Role(
            name="Administrator",
            level=RoleLevel.ADMIN,
            description="System administrator with operational control",
            permissions=[
                perm.id for perm in system_permissions 
                if perm.category in [PermissionCategory.USER, PermissionCategory.BUSINESS, PermissionCategory.DATA]
            ],
            is_system_role=True
        )
        
        manager_role = Role(
            name="Manager",
            level=RoleLevel.MANAGER,
            description="Business unit manager with operational oversight",
            permissions=[
                perm.id for perm in system_permissions 
                if perm.category in [PermissionCategory.BUSINESS, PermissionCategory.DATA]
            ],
            is_system_role=True
        )
        
        user_role = Role(
            name="User",
            level=RoleLevel.USER,
            description="Regular user with basic access",
            permissions=[
                perm.id for perm in system_permissions 
                if perm.category in [PermissionCategory.DATA]
            ],
            is_system_role=True
        )
        
        guest_role = Role(
            name="Guest",
            level=RoleLevel.GUEST,
            description="Limited access user",
            permissions=[],
            is_system_role=True
        )
        
        # Add roles to the system
        self.roles[founder_role.id] = founder_role
        self.roles[executive_role.id] = executive_role
        self.roles[architect_role.id] = architect_role
        self.roles[admin_role.id] = admin_role
        self.roles[manager_role.id] = manager_role
        self.roles[user_role.id] = user_role
        self.roles[guest_role.id] = guest_role
    
    def add_role(self, role: Role) -> bool:
        """
        Add a new role to the system
        
        Args:
            role: Role to add
            
        Returns:
            True if successful, False otherwise
        """
        if role.id in self.roles:
            return False
        
        self.roles[role.id] = role
        return True
    
    def get_role(self, role_id: str) -> Optional[Role]:
        """
        Get a role by ID
        
        Args:
            role_id: Role ID
            
        Returns:
            Role object or None if not found
        """
        return self.roles.get(role_id)
    
    def get_role_by_name(self, name: str) -> Optional[Role]:
        """
        Get a role by name
        
        Args:
            name: Role name
            
        Returns:
            Role object or None if not found
        """
        for role in self.roles.values():
            if role.name.lower() == name.lower():
                return role
        return None
    
    def update_role(self, role_id: str, updates: dict) -> bool:
        """
        Update a role
        
        Args:
            role_id: Role ID to update
            updates: Dictionary of updates
            
        Returns:
            True if successful, False otherwise
        """
        if role_id not in self.roles:
            return False
        
        role = self.roles[role_id]
        for key, value in updates.items():
            if hasattr(role, key):
                setattr(role, key, value)
        
        role.updated_at = datetime.utcnow()
        return True
    
    def delete_role(self, role_id: str) -> bool:
        """
        Delete a role
        
        Args:
            role_id: Role ID to delete
            
        Returns:
            True if successful, False otherwise
        """
        if role_id not in self.roles:
            return False
        
        role = self.roles[role_id]
        if role.is_system_role:
            return False  # Cannot delete system roles
        
        del self.roles[role_id]
        return True
    
    def add_permission(self, permission: Permission) -> bool:
        """
        Add a new permission
        
        Args:
            permission: Permission to add
            
        Returns:
            True if successful, False otherwise
        """
        if permission.id in self.permissions:
            return False
        
        self.permissions[permission.id] = permission
        return True
    
    def get_permission(self, permission_id: str) -> Optional[Permission]:
        """
        Get a permission by ID
        
        Args:
            permission_id: Permission ID
            
        Returns:
            Permission object or None if not found
        """
        return self.permissions.get(permission_id)
    
    def check_permission(self, user_roles: List[str], resource: str, action: str) -> bool:
        """
        Check if user has permission for a specific resource and action
        
        Args:
            user_roles: List of user role IDs
            resource: Resource to access
            action: Action to perform
            
        Returns:
            True if user has permission, False otherwise
        """
        for role_id in user_roles:
            role = self.roles.get(role_id)
            if not role:
                continue
            
            for perm_id in role.permissions:
                permission = self.permissions.get(perm_id)
                if not permission:
                    continue
                
                # Check if permission matches resource and action
                if (permission.resource == resource or permission.resource == "*") and \
                   (permission.action == action or permission.action == "all"):
                    return True
        
        return False
    
    def get_user_permissions(self, user_roles: List[str]) -> Set[str]:
        """
        Get all permissions for a user based on their roles
        
        Args:
            user_roles: List of user role IDs
            
        Returns:
            Set of permission names
        """
        permissions = set()
        
        for role_id in user_roles:
            role = self.roles.get(role_id)
            if not role:
                continue
            
            for perm_id in role.permissions:
                permission = self.permissions.get(perm_id)
                if permission:
                    permissions.add(f"{permission.resource}:{permission.action}")
        
        return permissions
    
    def get_inherited_roles(self, role_level: RoleLevel) -> List[RoleLevel]:
        """
        Get all roles that inherit from a given role level
        
        Args:
            role_level: Base role level
            
        Returns:
            List of inherited role levels
        """
        return self.role_hierarchy.get(role_level, [])
    
    def can_manage_role(self, manager_roles: List[str], target_role_id: str) -> bool:
        """
        Check if a user can manage a specific role
        
        Args:
            manager_roles: List of manager role IDs
            target_role_id: Target role ID to manage
            
        Returns:
            True if user can manage the role, False otherwise
        """
        target_role = self.roles.get(target_role_id)
        if not target_role:
            return False
        
        # Check if any manager role is higher in hierarchy than target role
        for manager_role_id in manager_roles:
            manager_role = self.roles.get(manager_role_id)
            if not manager_role:
                continue
            
            if manager_role.level in self.get_inherited_roles(target_role.level):
                return True
        
        return False
