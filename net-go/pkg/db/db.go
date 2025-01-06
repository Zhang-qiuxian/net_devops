package db

import (
	"fmt"
	"gorm.io/driver/mysql"
	"gorm.io/driver/postgres"
	//"gorm.io/driver/sqlite"
	"github.com/glebarez/sqlite"
	"gorm.io/gorm"
	//_ "modernc.org/sqlite" // 使用纯 Go 的 SQLite 驱动
	"net-go/models" // 替换为你的项目路径
	"net-go/pkg/config"
	"net-go/pkg/logger"
)

var DB *gorm.DB

// Init 初始化数据库连接
func Init() (*gorm.DB, error) {
	cfg := config.GetConfig().Database

	var err error
	switch cfg.Type {
	case "mysql":
		DB, err = initMySQL(cfg)
	case "postgres":
		DB, err = initPostgreSQL(cfg)
	case "sqlite":
		DB, err = initSQLite(cfg)
	default:
		return nil, fmt.Errorf("不支持的数据库类型: %s", cfg.Type)
	}

	if err != nil {
		return nil, fmt.Errorf("无法初始化数据库连接: %w", err)
	}

	// 自动迁移模型
	if err := autoMigrate(); err != nil {
		return nil, fmt.Errorf("无法自动迁移模型: %w", err)
	}
	logger.ApiLogger.Info("自动迁移模型成功！")
	return DB, nil
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

// autoMigrate 自动迁移模型
func autoMigrate() error {
	return DB.AutoMigrate(
		&models.User{},
		// 添加其他模型
	)
}
