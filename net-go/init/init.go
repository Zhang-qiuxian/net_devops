package init

import (
	"github.com/spf13/viper"
	"gorm.io/driver/sqlite"
	"gorm.io/gorm"
	"log"
)

func SetupInit() {
	setupViper()
	setupDB()
}

func setupViper() {
	viper.SetConfigName("config") // 配置文件名称（无后缀）
	viper.SetConfigType("toml")   // 配置文件后缀，也可以是 json, toml, yaml, yml 等
	viper.AddConfigPath(".")      // 配置文件路径
	err := viper.ReadInConfig()
	if err != nil {
		log.Fatalf("read config failed: %v", err)
	}
}

func setupDB() *gorm.DB {
	db, err := gorm.Open(sqlite.Open("test.db"), &gorm.Config{})
	if err != nil {
		panic("failed to connect database")
	}
	return db
}
