pipeline {
    agent any

    stages 
	{
        stage('GetCode') 
		{
            steps 
			{           
                git 'https://github.com/wien996/CP1.B.DevopsCloudUnir.git'
            }
        }

        stage('Unit') 
		{
            steps 
			{
                catchError(buildResult: 'SUCCESS', stageResult: 'SUCCESS') 
				{
                    bat '''
                        SET PYTHONPATH=%WORKSPACE%
                        C:\\Users\\danie\\AppData\\Local\\Programs\\Python\\Python313\\Scripts\\pytest --junitxml=result-unit.xml test\\unit
                    '''
                    junit 'result*.xml'
                }
            }
        }	
        
        stage('Coverage') 
		{
            steps 
			{
                bat '''
                    SET PYTHONPATH=%WORKSPACE%
                    C:\\Users\\danie\\AppData\\Local\\Programs\\Python\\Python313\\Scripts\\coverage run --branch --source=app --omit=app\\__init__.py,app\\api.py -m pytest test\\unit
                    C:\\Users\\danie\\AppData\\Local\\Programs\\Python\\Python313\\Scripts\\coverage xml
                '''
                catchError(buildResult: 'UNSTABLE', stageResult: 'SUCCESS') 
				{
                    cobertura coberturaReportFile: 'coverage.xml', 
                        lineCoverageTargets: '95,85,0', // Líneas: rojo <85, amarillo 85-95, verde >95
                        conditionalCoverageTargets: '90,80,0' // Condiciones: rojo <80, amarillo 80-90, verde >90
                }
            }
        }
        
        stage('Static Analysis: flake8') 
		{
            steps 
			{
                bat '''
                    C:\\Users\\danie\\AppData\\Local\\Programs\\Python\\Python313\\Scripts\\flake8 --exit-zero --format=pylint app >flake8.out
                '''
                recordIssues tools: [flake8(name: 'Flake8', pattern: 'flake8.out')], 
                    qualityGates: [
                        [threshold: 8, type: 'TOTAL', unstable: true], // Amarillo si hallazgos >= 8
                        [threshold: 10, type: 'TOTAL', unstable: false] // Rojo si hallazgos >= 10
                    ]
            }
        }
        
        stage('Security Analysis: Bandit') 
		{
            steps 
			{
                bat '''
                    C:\\Users\\danie\\AppData\\Local\\Programs\\Python\\Python313\\Scripts\\bandit --exit-zero -r . -f custom -o bandit.out --msg-template  "{abspath}:{line}: [{test_id}] {msg}"
                '''
                recordIssues tools: [pyLint(name: 'Bandit', pattern: 'bandit.out')], 
                    qualityGates: [
                        [threshold: 2, type: 'TOTAL', unstable: true], // Amarillo si hallazgos >= 2
                        [threshold: 4, type: 'TOTAL', unstable: false] // Rojo si hallazgos >= 4
                    ]
            }
        }
        
        stage('Performance: JMeter') 
		{
            steps 
			{
                bat '''
                    C:\\Users\\danie\\AppData\\Local\\Programs\\apache-jmeter-5.6.3\\bin\\jmeter -n -t test\\jmeter\\flask.jmx -f -l flask.jtl
                '''
                perfReport sourceDataFiles: 'flask.jtl'
            }
        }
    }
}
