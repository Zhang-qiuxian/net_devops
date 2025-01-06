package main

import (
	"fmt"
	"github.com/gin-gonic/gin"
	"go.uber.org/zap"
	"log"
	"net-go/pkg/config"
	"net-go/pkg/db"
	"net-go/pkg/logger"
)

func main() {
	// 初始化配置
	if err := config.Init("config/config.yaml"); err != nil {
		log.Fatalf("Failed to initialize config: %v", err)
	}

	// 获取初始配置
	cfg := config.GetConfig()
	log.Printf("初始配置: %+v\n", cfg)

	// 初始化日志
	if err := logger.Init("logs"); err != nil {
		log.Fatalf("Failed to initialize logger: %v", err)
	}
	defer logger.Sync() // 确保程序退出时刷新日志缓冲区

	// 初始化数据库
	if err := db.Init(); err != nil {
		logger.Logger.Fatal("Failed to initialize database", zap.Error(err))
	}

	// 初始化 Gin
	r := gin.Default()

	// 示例路由
	r.GET("/config", func(c *gin.Context) {
		currentCfg := config.GetConfig()
		c.JSON(200, gin.H{
			"server":   currentCfg.Server,
			"database": currentCfg.Database,
		})
	})

	// 启动服务
	if err := r.Run(fmt.Sprintf("%s:%d", cfg.Server.Host, cfg.Server.Port)); err != nil {
		logger.Logger.Fatal("Failed to start server", zap.Error(err))
	}
}
