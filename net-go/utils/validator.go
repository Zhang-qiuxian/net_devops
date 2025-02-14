package utils

import (
	"github.com/gin-gonic/gin/binding"
	"github.com/go-playground/locales/zh"
	ut "github.com/go-playground/universal-translator"
	"github.com/go-playground/validator/v10"
	zhTranslations "github.com/go-playground/validator/v10/translations/zh"
)

var Trans ut.Translator

func InitValidator() {
	// 初始化中文翻译器
	zh := zh.New()
	uni := ut.New(zh, zh)

	// 设置全局翻译器
	Trans, _ = uni.GetTranslator("zh")

	// 获取 Gin 的校验器
	if v, ok := binding.Validator.Engine().(*validator.Validate); ok {
		// 注册中文翻译
		_ = zhTranslations.RegisterDefaultTranslations(v, Trans)
	}
}
