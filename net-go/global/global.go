package global

import (
	"github.com/spf13/viper"
	"gorm.io/gorm"
)

var (
	Viper *viper.Viper
	DB    *gorm.DB
)
