package config

import (
	"fmt"
	"gopkg.in/yaml.v3"
	"log"
	"os"
	"path/filepath"
	"sync"

	"github.com/fsnotify/fsnotify"
	"github.com/spf13/viper"
)

// Config 结构体定义
type Config struct {
	Server   ServerConfig
	Database DatabaseConfig
}

type ServerConfig struct {
	Host string `mapstructure:"host" yaml:"host" json:"host"`
	Port int    `mapstructure:"port" yaml:"port" json:"port"`
	Mode string `mapstructure:"mode" yaml:"mode" json:"mode"`
}

type DatabaseConfig struct {
	Host     string `mapstructure:"host" yaml:"host" json:"host"`
	Port     int    `mapstructure:"port" yaml:"port" json:"port"`
	Username string `mapstructure:"username" yaml:"username" json:"username"`
	Password string `mapstructure:"password" yaml:"password" json:"password"`
	Name     string `mapstructure:"name" yaml:"name" json:"name"`
	Type     string `mapstructure:"type" yaml:"type" json:"type"`
}

var (
	AppConfig  Config
	configLock sync.RWMutex
)

// Init 初始化 Viper 并加载配置文件
func Init(configPath string) error {
	// 获取绝对路径
	absPath, err := filepath.Abs(configPath)
	if err != nil {
		return fmt.Errorf("无法获取配置文件绝对路径: %w", err)
	}

	// 确保目录存在
	if err := os.MkdirAll(filepath.Dir(absPath), os.ModePerm); err != nil {
		return fmt.Errorf("无法创建配置目录: %w", err)
	}

	// 检查配置文件是否存在
	if _, err := os.Stat(absPath); os.IsNotExist(err) {
		// 配置文件不存在，创建默认配置文件
		fmt.Println("配置文件不存在，创建默认配置文件...")
		if err := createDefaultConfig(absPath); err != nil {
			return fmt.Errorf("无法创建默认配置文件: %w", err)
		}
	}

	// 设置配置文件路径
	viper.SetConfigFile(configPath)

	// 读取配置文件
	if err := viper.ReadInConfig(); err != nil {
		return fmt.Errorf("无法读取配置文件: %w", err)
	}

	// 解析配置文件到结构体
	if err := viper.Unmarshal(&AppConfig); err != nil {
		return fmt.Errorf("无法解析配置文件: %w", err)
	}

	// 监听配置文件变化
	viper.WatchConfig()
	viper.OnConfigChange(func(e fsnotify.Event) {
		fmt.Println("配置文件已更改，重新加载配置...")
		configLock.Lock()
		defer configLock.Unlock()
		if err := viper.Unmarshal(&AppConfig); err != nil {
			fmt.Printf("重新加载配置失败: %v\n", err)
		}
	})

	return nil
}

// GetConfig 返回全局配置
func GetConfig() Config {
	configLock.RLock()
	defer configLock.RUnlock()
	return AppConfig
}

// 创建默认配置文件
func createDefaultConfig(configPath string) error {
	// 初始化结构体
	cfg := Config{
		Server: ServerConfig{
			Host: "localhost",
			Port: 8080,
			Mode: "debug",
		},
		Database: DatabaseConfig{
			Host:     "127.0.0.1",
			Port:     3306,
			Username: "root",
			Password: "password",
			Name:     "db.sqlite3",
			Type:     "sqlite3",
		},
	}

	// 将结构体转换为 YAML
	yamlData, err := yaml.Marshal(&cfg)
	if err != nil {
		log.Fatalf("无法将结构体转换为 YAML: %v", err)
		return err
	}

	if err := os.WriteFile(configPath, yamlData, 0644); err != nil {
		log.Fatalf("无法写入 YAML 文件: %v", err)
		return err
	}

	fmt.Printf("配置文件已成功写入: %s\n", configPath)
	return nil
}
