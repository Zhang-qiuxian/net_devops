package api

import (
	"fmt"
	"github.com/gin-gonic/gin"
	"github.com/go-playground/validator/v10"
	"golang.org/x/crypto/bcrypt"
	"gorm.io/gorm"
	"net-go/middleware"
	"net-go/models"
	"net-go/pkg/jwt"
	"net-go/utils"
	"net/http"
	"reflect"
)

// RegisterRequest 注册请求体
type RegisterRequest struct {
	Username string `json:"username"  binding:"required,min=2,max=100" validate:"required"`
	Password string `json:"password"  binding:"required" validate:"required"`
	Email    string `json:"email"  binding:"required,email" validate:"required"`
}

// LoginRequest 登录请求体
type LoginRequest struct {
	Username string `json:"username" validate:"required"`
	Password string `json:"password" validate:"required"`
}

// Register 用户注册
func Register(c *gin.Context) {
	var req RegisterRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		fmt.Println(reflect.TypeOf(err))
		// 校验参数
		validate := validator.New()
		fmt.Println("校验开始")
		if err := validate.Struct(req); err != nil {
			fmt.Println("????进来了")
			errs := err.(validator.ValidationErrors)
			fmt.Println(errs)
			translatedErrs := make(map[string]string)
			for _, e := range errs {
				translatedErrs[e.Field()] = e.Translate(utils.Trans) // 翻译错误信息
			}
			fmt.Println(translatedErrs)
			c.JSON(http.StatusBadRequest, gin.H{"error": translatedErrs})
			return
		}
		middleware.HandleValidationError(c, err)
		return
	}
	// 检查用户名是否已存在
	var existingUser models.User
	db := c.MustGet("db").(*gorm.DB)
	if err := db.Where("username = ?", req.Username).First(&existingUser).Error; err == nil {
		c.JSON(http.StatusBadRequest, gin.H{
			"message": "用户已存在!",
			"data":    err,
		})
		return
	}

	// 加密密码
	hashedPassword, err := bcrypt.GenerateFromPassword([]byte(req.Password), bcrypt.DefaultCost)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{
			"message": "Failed to hash password",
		})
		return
	}

	// 创建用户
	user := &models.User{
		Username: req.Username,
		Password: string(hashedPassword),
		Email:    req.Email,
		Status:   "active",
	}
	fmt.Println("走到这里了")
	fmt.Println(user)
	// 校验参数
	validate := validator.New()
	fmt.Println("校验开始")
	if err := validate.Struct(user); err != nil {
		fmt.Println("????进来了")
		errs := err.(validator.ValidationErrors)
		fmt.Println(errs)
		translatedErrs := make(map[string]string)
		for _, e := range errs {
			translatedErrs[e.Field()] = e.Translate(utils.Trans) // 翻译错误信息
		}
		fmt.Println(translatedErrs)
		c.JSON(http.StatusBadRequest, gin.H{"error": translatedErrs})
		return
	}
	fmt.Println("校验结束了")
	if err := db.Create(&user).Error; err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{
			"message": "创建失败!",
			"data":    err.Error(),
		})
		return
	}

	c.JSON(http.StatusOK, gin.H{
		"message": "注册成功!",
		"data":    user,
	})
}

// Login 用户登录
func Login(c *gin.Context) {
	var req LoginRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		// 校验参数
		validate := validator.New()
		if err := validate.Struct(req); err != nil {
			errs := err.(validator.ValidationErrors)
			translatedErrs := make(map[string]string)
			for _, e := range errs {
				translatedErrs[e.Field()] = e.Translate(utils.Trans) // 翻译错误信息
			}
			c.JSON(http.StatusBadRequest, gin.H{
				"message": "Invalid request",
				"error":   translatedErrs})
			return
		}
	}

	// 查询用户
	var user models.User
	db := c.MustGet("db").(*gorm.DB)
	if err := db.Where("username = ?", req.Username).First(&user).Error; err != nil {
		c.JSON(http.StatusUnauthorized, gin.H{
			"message": "用户不存在",
			"data":    err,
		})
		return
	}

	// 验证密码
	if err := bcrypt.CompareHashAndPassword([]byte(user.Password), []byte(req.Password)); err != nil {
		c.JSON(http.StatusUnauthorized, gin.H{
			"message": "密码不正确！",
			"data":    err,
		})
		return
	}

	// 签发 Token
	token, err := jwt.GenerateToken(int(user.ID), user.Username)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{
			"message": "token生成失败！",
			"data":    err,
		})
		return
	}

	c.JSON(http.StatusOK, gin.H{
		"token": token,
		"user":  user,
	})
}
