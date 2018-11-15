#!/usr/bin/python
# -*- coding:utf-8 -*-
# N皇后问题求解---回溯法
import random
import sys
# 冲突检测，定义state元组为皇后的位置，next_x为下一个皇后的横坐标（即所在列）
# 如state[1] = 2表示，皇后的位置处在第二行第三列。


def conflict(state, next_x):
	next_y = len(state)
	for i in range(next_y):
		# 如果下一个皇后位置与每个放置的皇后位置在同一列或者在同一对角线上，则表示冲突
		if abs(state[i] - next_x) in (0, next_y - i):
			return True
	return False
# 生成器递归生成皇后的位置


def queens(num, state=()):
	for pos in range(num):
		if not conflict(state,pos):
			# 递归的出口，产生皇后的位置
			if len(state) == num - 1:
				yield (pos,)
			else:
				# 将当前的皇后位置添加到state中并传递给下一个皇后
				for result in queens(num, state + (pos,)):
					yield (pos,) + result
# 使用棋盘布局直观显示结果，其中Q表示皇后位置


def pretty_print(solution):
	def line(position, length=len(solution)):
		return '. ' * position + 'Q ' + '. ' * (length - pos - 1)
	for pos in solution:
		print line(pos)
# 随机的显示一种结果


if __name__ == '__main__':
	x_num = int(sys.argv[1])
	solution_list = list(queens(x_num))
	print "total solution num:", len(solution_list)
	print "one of solution:"
	pretty_print(random.choice(solution_list))
