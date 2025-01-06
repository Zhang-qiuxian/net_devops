package init

import (
	"fmt"
	"os"

	"github.com/spf13/viper"
	"gorm.io/driver/sqlite"
	"gorm.io/gorm"
)

func SetupInit() {
	setupViper()
	setupDB()
}

// 默认配置文件内容
const defaultConfig = `
server:
  host: "localhost"
  port: 8080

debug: true
`

func setupViper() {
	// 设置配置文件名称和类型
	viper.SetConfigName("config") // 配置文件名称（不需要扩展名）
	viper.SetConfigType("yaml")   // 配置文件类型
	viper.AddConfigPath(".")      // 配置文件路径

	// 检查配置文件是否存在
	if err := viper.ReadInConfig(); err != nil {
		if _, ok := err.(viper.ConfigFileNotFoundError); ok {
			// 配置文件不存在，创建默认配置文件
			fmt.Println("配置文件不存在，创建默认配置文件...")
			if err := createDefaultConfig(); err != nil {
				panic(fmt.Errorf("无法创建默认配置文件: %s \n", err))
			}
			// 重新读取配置文件
			if err := viper.ReadInConfig(); err != nil {
				panic(fmt.Errorf("无法读取配置文件: %s \n", err))
			}
		} else {
			// 其他错误
			panic(fmt.Errorf("配置文件错误: %s \n", err))
		}
	}

	// 读取配置项
	host := viper.GetString("server.host")
	port := viper.GetInt("server.port")
	debug := viper.GetBool("debug")

	// 打印配置项
	fmt.Printf("Host: %s\n", host)
	fmt.Printf("Port: %d\n", port)
	fmt.Printf("Debug: %v\n", debug)
}

// 创建默认配置文件
func createDefaultConfig() error {
	// 创建文件
	file, err := os.Create("config.yaml")
	if err != nil {
		return err
	}
	defer file.Close()

	// 写入默认配置内容
	_, err = file.WriteString(defaultConfig)
	if err != nil {
		return err
	}

	fmt.Println("默认配置文件已创建：config.yaml")
	return nil
}

func setupDB() *gorm.DB {
	db, err := gorm.Open(sqlite.Open("test.db"), &gorm.Config{})
	if err != nil {
		panic("failed to connect database")
	}
	return db
}
