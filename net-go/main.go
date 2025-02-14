package main

import (
	"fmt"
	"github.com/gin-gonic/gin"
	"go.uber.org/zap"
	"log"
	"net-go/api"
	"net-go/middleware"
	"net-go/pkg/config"
	"net-go/pkg/db"
	"net-go/pkg/logger"
	"net-go/utils"
	"net/http"
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
	DB, err := db.Init()
	if err != nil {
		logger.ErrorLogger.Fatal("Failed to initialize database", zap.Error(err))
	}

	// 初始化校验器和翻译器
	utils.InitValidator()

	// 初始化 Gin
	r := gin.Default()

	// 将数据库实例注入 Gin 上下文
	r.Use(func(c *gin.Context) {
		c.Set("db", DB)
		c.Next()
	})

	// 注册路由
	r.POST("/register", api.Register)
	r.POST("/login", api.Login)
	// 受保护的路由
	authGroup := r.Group("/api")
	authGroup.Use(middleware.AuthMiddleware())
	{
		authGroup.GET("/profile", func(c *gin.Context) {
			userID := c.GetUint("user_id")
			username := c.GetString("username")

			c.JSON(http.StatusOK, gin.H{
				"user_id":  userID,
				"username": username,
			})
		})
	}

	// 启动服务
	if err := r.Run(fmt.Sprintf("%s:%d", cfg.Server.Host, cfg.Server.Port)); err != nil {
		logger.ErrorLogger.Fatal("Failed to start server", zap.Error(err))
	}
}
