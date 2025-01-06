package db

import (
	"fmt"
	"gorm.io/driver/mysql"
	"gorm.io/driver/postgres"
	"gorm.io/driver/sqlite"
	"gorm.io/gorm"
	_ "modernc.org/sqlite"
	"net-go/models"
	"net-go/pkg/config" // 替换为你的项目路径

	_ "github.com/go-sql-driver/mysql" // MySQL 驱动
	_ "github.com/lib/pq"              // PostgreSQL 驱动
	//"gorm.io/driver/postgres"
)

var DB *gorm.DB

// Init 初始化数据库连接
func Init() error {
	cfg := config.GetConfig().Database

	var err error
	switch cfg.Type {
	case "mysql":
		DB, err = initMySQL(cfg)
	case "postgres":
		DB, err = initPostgreSQL(cfg)
	case "sqlite3":
		DB, err = initSQLite(cfg)
	default:
		return fmt.Errorf("不支持的数据库类型: %s", cfg.Type)
	}

	if err != nil {
		return fmt.Errorf("无法初始化数据库连接: %w", err)
	}

	// 测试数据库连接
	sqlDB, err := DB.DB()
	if err != nil {
		return fmt.Errorf("无法获取数据库实例: %w", err)
	}
	if err := sqlDB.Ping(); err != nil {
		return fmt.Errorf("数据库连接测试失败: %w", err)
	}

	fmt.Println("数据库连接成功")
	// 自动迁移模型
	if err := DB.AutoMigrate(&models.User{}); err != nil {
		return fmt.Errorf("无法自动迁移模型: %w", err)
	}
	fmt.Println("数据库迁移成功")
	return nil
}

// initMySQL 初始化 MySQL 连接
func initMySQL(cfg config.DatabaseConfig) (*gorm.DB, error) {
	dsn := fmt.Sprintf("%s:%s@tcp(%s:%d)/%s?charset=utf8mb4&parseTime=True&loc=Local",
		cfg.Username, cfg.Password, cfg.Host, cfg.Port, cfg.Name)
	return gorm.Open(mysql.Open(dsn), &gorm.Config{})
}

// initPostgreSQL 初始化 PostgreSQL 连接
func initPostgreSQL(cfg config.DatabaseConfig) (*gorm.DB, error) {
	dsn := fmt.Sprintf("host=%s port=%d user=%s password=%s dbname=%s sslmode=disable",
		cfg.Host, cfg.Port, cfg.Username, cfg.Password, cfg.Name)
	return gorm.Open(postgres.Open(dsn), &gorm.Config{})
}

// initSQLite 初始化 SQLite 连接
func initSQLite(cfg config.DatabaseConfig) (*gorm.DB, error) {
	return gorm.Open(sqlite.Open(cfg.Name), &gorm.Config{})
}
