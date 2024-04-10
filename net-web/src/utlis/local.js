class LocalStorageManager {
    constructor(prefix = '') {
        this.prefix = prefix;
    }

    // 设置数据  
    setItem(key, value) {
        const prefixedKey = this.getPrefixedKey(key);
        try {
            localStorage.setItem(prefixedKey, JSON.stringify(value));
            return true;
        } catch (error) {
            console.error('Error setting item in localStorage:', error);
            return false;
        }
    }

    // 获取数据  
    getItem(key) {
        const prefixedKey = this.getPrefixedKey(key);
        try {
            const item = localStorage.getItem(prefixedKey);
            return item ? JSON.parse(item) : null;
        } catch (error) {
            console.error('Error getting item from localStorage:', error);
            return null;
        }
    }

    // 删除数据  
    removeItem(key) {
        const prefixedKey = this.getPrefixedKey(key);
        try {
            localStorage.removeItem(prefixedKey);
            return true;
        } catch (error) {
            console.error('Error removing item from localStorage:', error);
            return false;
        }
    }

    // 获取带有前缀的键  
    getPrefixedKey(key) {
        return `${this.prefix}${key}`;
    }

    // 检查是否存在某个键  
    hasItem(key) {
        const prefixedKey = this.getPrefixedKey(key);
        return localStorage.getItem(prefixedKey) !== null;
    }

    // 清除所有数据  
    clear() {
        try {
            localStorage.clear();
            return true;
        } catch (error) {
            console.error('Error clearing localStorage:', error);
            return false;
        }
    }
}

// 使用示例  
// const lsManager = new LocalStorageManager('myApp_'); // 为键添加前缀，避免与其他应用的数据冲突  

// // 设置数据  
// lsManager.setItem('user', { name: 'John Doe', age: 30 });

// // 获取数据  
// const user = lsManager.getItem('user');
// console.log(user); // { name: 'John Doe', age: 30 }  

// // 删除数据  
// lsManager.removeItem('user');

// // 检查数据是否存在  
// const hasUser = lsManager.hasItem('user');
// console.log(hasUser); // false  

// // 清除所有数据  
// lsManager.clear();

const lsManager = new LocalStorageManager('net_devops_');

export {lsManager}