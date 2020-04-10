import demjson

inputdata = """
{
    region: {
        name: "Africa",
        avgAge: 19.7,
        avgDailyIncomeInUSD: 5,
        avgDailyIncomePopulation: 0.71
    },
    periodType: "days",
    timeToElapse: 58,
    reportedCases: 674,
    population: 66622705,
    totalHospitalBeds: 1380614
}
"""


def estimator(data):
    data = demjson.decode(data)
    impact = {}
    severeImpact = {}

    reportedCases = data['reportedCases']
    totalHospitalBeds = data['totalHospitalBeds']
    avgIncome = 1.5
    period = 30
    majority = 0.65

    # currently infected
    impact['currentlyInfected'] = reportedCases * 10
    severeImpact['currentlyInfected'] = reportedCases * 50

    # infections by requested time
    impact['infectionsByRequestedTime'] = \
        impact['currentlyInfected'] * (2 ** (period // 3))
    severeImpact['infectionsByRequestedTime'] = \
        severeImpact['currentlyInfected'] * (2 ** (period // 3))

    # sever cases by requested time
    impact['severeCasesByRequestedTime'] = \
        int(0.15 * impact['infectionsByRequestedTime'])
    severeImpact['severeCasesByRequestedTime'] = \
        int(0.15 * severeImpact['infectionsByRequestedTime'])

    # hospital beds by requested time
    availability = 0.35
    impact['hospitalBedsByRequestedTime'] = \
        impact['severeCasesByRequestedTime'] - \
        int(availability * totalHospitalBeds)
    severeImpact['hospitalBedsByRequestedTime'] = \
        severeImpact['severeCasesByRequestedTime'] - \
        int(availability * totalHospitalBeds)

    # require ICU care
    impact['casesForICUByRequestedTime'] = \
        int(0.05 * impact['infectionsByRequestedTime'])
    severeImpact['casesForICUByRequestedTime'] = \
        int(0.05 * severeImpact['infectionsByRequestedTime'])

    # require ventilators
    impact['casesForVentilatorsByRequestedTime'] = \
        int(0.02 * impact['infectionsByRequestedTime'])
    severeImpact['casesForVentilatorsByRequestedTime'] = \
        int(0.02 * severeImpact['infectionsByRequestedTime'])

    # money lost by the economy
    impact['dollarsInFlight'] = \
        impact['infectionsByRequestedTime'] * majority * avgIncome * period
    severeImpact['dollarsInFlight'] = \
        severeImpact['infectionsByRequestedTime'] * \
        majority * avgIncome * period

    print(data)
    print(impact)
    print(severeImpact)

    dicts = {data, impact, severeImpact}
    data = demjson.encode(dicts)

    return data


print(estimator(inputdata))
