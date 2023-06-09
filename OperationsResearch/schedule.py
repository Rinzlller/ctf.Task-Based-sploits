#!/usr/bin/env python3


def main():
	
	groupCount = 4
	professorCount = 8
	roomCount = 2
	workDays = 6
	workHours = 4

	timeline = workDays*workHours

	# isProfessorFree[professorCount][workDays*workHours]
	# isProfessorFree = [ [1 for _ in range(timeline)] for I in range(professorCount)]
	isProfessorFree = [
	[0,0,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,1,1,1],
	[1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1],
	[1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,0],
	[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
	[0,0,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,1,1,1],
	[1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1],
	[1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,0],
	[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
	]

	# isPlanned[groupCount][professorCount]
	isPlanned = [
		[4,4,2,4,0,0,0,0],		# group 1
		[4,4,2,4,0,0,0,0],		# group 2
		[0,0,0,0,4,4,2,4],		# group 3
		[0,0,0,0,4,4,2,4],		# group 4
	]

	# isLessonPossible[groupCount][professorCount][roomCount]
	isLessonPossible = [ [ [1 for _ in range(roomCount)] for _ in range(professorCount)] for _ in range(groupCount)]

	# groupTimeline[groupCount][workDays*workHours]
	groupTimeline = [ [0 for _ in range(timeline)] for _ in range(groupCount)]

	# roomTimeline[roomCount][workDays*workHours]
	roomTimeline = [ [0 for _ in range(timeline)] for _ in range(roomCount)]

	for j in range(professorCount):
		for t in range(timeline):

			if isProfessorFree[j][t] == 0:
				continue

			isLessonCompleted = False
			for i in range(groupCount):

				if isPlanned[i][j] == 0:
					continue

				for k in range(roomCount):

					if isLessonPossible[i][j][k] == 0:
						continue
				
					if (groupTimeline[i][t] != 1) and (roomTimeline[k][t] != 1):

						print(f"Lecture: {t+1}\t\tProfessor: {j+1}\tGroup: {i+1}\tAuditory: {k+1}")

						groupTimeline[i][t] = 1
						roomTimeline[k][t] = 1

						isPlanned[i][j] -= 1
						isProfessorFree[j][t] = 0

						isLessonCompleted = True
						break

				if isLessonCompleted:
					break


if __name__ == "__main__":
    main()