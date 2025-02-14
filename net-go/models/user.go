package models

import (
	"gorm.io/gorm"
	"time"
)

type User struct {
	gorm.Model
	Username  string    `gorm:"uniqueIndex;not null" json:"username" binding:"required" validate:"required"`
	Password  string    `gorm:"not null" json:"-" binding:"required" validate:"required"`
	Email     string    `gorm:"uniqueIndex" json:"email" binding:"required" validate:"required"`
	Status    string    `gorm:"default:'active'" json:"status" binding:"required" validate:"required"` // 用户状态：active, inactive
	CreatedAt time.Time `json:"created_at"`
	UpdatedAt time.Time `json:"updated_at"`
}

func (User) TableName() string {
	return "user"
}
