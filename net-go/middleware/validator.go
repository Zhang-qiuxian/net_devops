package middleware

import (
	"net/http"

	"github.com/gin-gonic/gin"
	"github.com/go-playground/locales/zh"
	ut "github.com/go-playground/universal-translator"
	"github.com/go-playground/validator/v10"
	zh_translations "github.com/go-playground/validator/v10/translations/zh"
)

var (
	validate *validator.Validate
	trans    ut.Translator
)

func init() {
	// 初始化校验器和翻译器
	validate = validator.New()
	zh := zh.New()
	uni := ut.New(zh, zh)
	trans, _ = uni.GetTranslator("zh")

	// 注册中文翻译
	_ = zh_translations.RegisterDefaultTranslations(validate, trans)
}

// ValidationError 自定义校验错误结构
type ValidationError struct {
	Field   string `json:"field"`
	Message string `json:"message"`
}

// HandleValidationError 处理参数校验失败的错误
func HandleValidationError(c *gin.Context, err error) {
	var errors []ValidationError

	// 判断错误类型
	if validationErrors, ok := err.(validator.ValidationErrors); ok {
		for _, e := range validationErrors {
			errors = append(errors, ValidationError{
				Field:   e.Field(),
				Message: e.Translate(trans), // 翻译错误信息
			})
		}
	} else {
		// 如果不是校验错误，返回通用错误信息
		errors = append(errors, ValidationError{
			Field:   "unknown",
			Message: err.Error(),
		})
	}

	// 返回 JSON 响应
	c.JSON(http.StatusBadRequest, gin.H{
		"message": "参数校验失败",
		"errors":  errors,
	})
}
